# ReviewboardExtensions

## ci_approval_extension
  This extension is intended to be used with mercurial-reviewboard or similar plugin which scans approved reviews for automated code integration to remote repository and review request closing. Also it is intended to be used with CI (like jenkins) tool for code quality check. This tool should be able to comment on review via Reviewboard API directly or some plugin (like Jenkins-Reviewbot).</br>
  By default Reviewboard marks request as approved when it has at least one "Ship it!" comment (marked with ship_it flag). This extension extends approving by following, more strict, conditions:
  * At least one "Ship it!" (ship_it flag) comment exists after latest diff update.
  * At least one CI comment (Starting with "Congratulations, Jenkins successfully built the changes.") exists after latest diff update.
  Needed improvements:
  * Admin configuration page creation
  * Required CI comment extraction to configuration page and default parameters
  * Hardcoded "Genesis" repository name extraction to configuration page and default parameters (default should be blanc and enabled for all repositories, currently only on repository named "Genesis" extension will work)
  
## Installation
* Download extension to your reviewboard linux server with pip installed
* Run "pip install -U ./" from extensions directory
