from contrib.tools.eis_extension.eis_extension.extension import EisApprovalExtension
from reviewboard.extensions.testing import ExtensionTestCase
from reviewboard.reviews.models import review_request


class EisApprovalExtensionTests(ExtensionTestCase):

    extension_class = EisApprovalExtension

    def test_something(self):
        prev_approved = True
        prev_failure = None
        self.assertEqual(self.extension.is_approved(self, review_request, prev_approved, prev_failure), True)