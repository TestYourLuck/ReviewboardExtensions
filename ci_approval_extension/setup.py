from __future__ import unicode_literals

from reviewboard.extensions.packaging import setup

from eis_extension import get_package_version


PACKAGE = "eis_extension"

setup(
    name=PACKAGE,
    version=get_package_version(),
    description="EIS extension for modifying reviewboard approvals.",
    author="Daumantas Stulgis",
    packages=['eis_extension'],
    entry_points={
        'reviewboard.extensions': [
            'eis_extension = eis_extension.extension:EisApprovalExtension',
        ],
    }
)