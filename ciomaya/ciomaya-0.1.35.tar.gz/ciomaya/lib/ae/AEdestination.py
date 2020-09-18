"""
Handle the UI for extra assets:
"""

import pymel.core as pm
from ciomaya.lib import const as k

from ciomaya.lib.ae import AEcommon


def create_ui(node_attr):
    """Build static UI.
    """
    attr = pm.Attribute(node_attr)
    with AEcommon.ae_template():

        form = pm.formLayout("ddFormName", nd=100)

        field = pm.attrControlGrp("destinationField", attribute=node_attr)

        button = pm.symbolButton(
            "destinationButton",
            image="SP_DirClosedIcon.png", width=24, height=24
        )
        pm.setParent("..")  # out of formLayout

        form.attachNone(button, "left")
        form.attachForm(button, "right", 2)
        form.attachForm(button, "top", 2)
        form.attachForm(button, "bottom", 2)

        form.attachForm(field, "left", 2)
        form.attachControl(field, "right", 2, button)
        form.attachForm(field, "top", 2)
        form.attachForm(field, "bottom", 2)

        populate_ui(node_attr)


def populate_ui(node_attr):
    """Reconfigure action buttons when node changes."""
    widgets = _get_widgets()

    attr = pm.Attribute(node_attr)

    pm.attrControlGrp("destinationField", edit=True, en=True, attribute=node_attr)

    pm.symbolButton(
        widgets["button"],
        edit=True,
        command=pm.Callback(_on_browse_button, attr,  widgets["field"]),
    )


def _get_widgets(parent=None):
    if not parent:
        parent = pm.setParent(q=True)
    return {
        "field":  AEcommon.find_ui("destinationField", parent),
        "button": AEcommon.find_ui("destinationButton", parent)
    }


def _on_browse_button(attr, field):
    path = browse_for_dest_directory()
    if path:
        attr.set(path)
        AEcommon.print_setAttr_cmd(attr)


def browse_for_dest_directory():
    entries = pm.fileDialog2(
        caption="Choose Directory",
        okCaption="Choose",
        fileFilter="*",
        dialogStyle=2,
        fileMode=3,
        dir=pm.workspace.getPath(),
    )
    if entries:
        return entries[0]
    pm.displayWarning("No files Selected")
