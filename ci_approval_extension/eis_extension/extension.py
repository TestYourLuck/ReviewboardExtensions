# EIS approval hook extension for Review Board.
from __future__ import unicode_literals


from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import ReviewRequestApprovalHook

import logging

class EisApprovalHook(ReviewRequestApprovalHook):
    def is_approved(self, review_request, prev_approved, prev_failure):
        logging.debug('[EAH]  EIS Aproval hook triggered for review request #%s' % review_request.id)
        
        # If default approval not passed, then return
        if not prev_approved:
            logging.debug('[EAH]  Previous approval did not pass')
            return prev_approved, prev_failure
        
        # If repository not 'Genesis', then return
        if review_request.repository.name != 'Genesis':
            logging.debug('[EAH]  Review repository is not "Genesis"')
            return False, 'Only for Genesis repository EIS approval hook is enabled.'
        
        # Scan for Jenkins comment and Ship it flag
        logging.debug('[EAH]  Searching for "Ship it!" and CI comments...')
        
        latest_diffset = review_request.get_latest_diffset()
        shipit_reviews = [r for r in review_request.reviews.all() if r.ship_it]
        comment_reviews = [r for r in review_request.reviews.all() if r.body_top.startswith('Congratulations, Jenkins successfully built the changes.')]
        
        
        if not comment_reviews:
            logging.debug('[EAH]  No CI comments found...')
            return False, 'Review request has not passed CI regression!'
        
        if not latest_diffset: # refactor for new requests
            logging.debug('[EAH]  Diff not found...')
            return False, 'Review request has no diff!'
            
        if not shipit_reviews:
            logging.debug('[EAH]  Ship it flgs not found...')
            return False, 'Review request was not shipped!'
        
        # Default approval checked at this point, so at least one "Ship it!" flag exists.
        # Check if ship_it exists after latest diff
        if latest_diffset and shipit_reviews:
            for shipit in shipit_reviews:
                if shipit.timestamp < latest_diffset.timestamp:
                    logging.debug('[EAH]  Latest "Ship it!" time is older than latest diff added: %s < %s ...' % (shipit.timestamp, latest_diffset.timestamp))
                    return False, 'The latest diff has not been marked "Ship It!"'
            logging.debug('[EAH]  "Ship it!" found. Searching for CI comment...')
        
        # Check if CI passed after latest diff
        if latest_diffset and comment_reviews:
            for comment in comment_reviews:
                if comment.timestamp < latest_diffset.timestamp:
                    logging.debug('[EAH]  Latest CI regression passing comment is older than latest diff added: %s < %s ...' % (comment.timestamp, latest_diffset.timestamp))
                    return False, 'The latest diff has not passed CI regression!'
        
        logging.debug('[EAH]  "Ship it!" and CI comments found. Review #%s approved.' % review_request.id)
        return True
    

class EisApprovalExtension(Extension):
    metadata = {
        'Name': 'EisApprovalExtension',
        'Summary': 'Does additional checking if review request should be shipped based on CI job comment.',
        'Author': 'Daumantas Stulgisis',
        'Author-email': 'dstulgis@eisgroup.com',
    }
    
    def initialize(self):
        EisApprovalHook(self)
