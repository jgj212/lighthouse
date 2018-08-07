import logging

from binaryninja import HighlightStandardColor
from binaryninja.highlight import HighlightColor

from lighthouse.util.disassembler import disassembler
from lighthouse.painting import DatabasePainter

logger = logging.getLogger("Lighthouse.Painting")

class BinjaPainter(DatabasePainter):
    """
    Asynchronous Binary Ninja database painter.
    """

    def __init__(self, director, palette):
        super(BinjaPainter, self).__init__(director, palette)

    #------------------------------------------------------------------------------
    # Paint Actions
    #------------------------------------------------------------------------------

    # TODO/BINJA: these technicallly need to be called in a background task...

    def _paint_instructions(self, instructions):
        """
        Paint instruction level coverage defined by the current database mapping.

        Internal routine to force called action to the main thread.
        """
        bv = disassembler.bv
        for address in instructions:
            for func in bv.get_functions_containing(address):
                # TODO/BINJA:  self.palette.ida_coverage
                func.set_auto_instr_highlight(address, HighlightStandardColor.BlueHighlightColor)
        self._painted_instructions |= set(instructions)
        self._action_complete.set()

    def _clear_instructions(self, instructions):
        """
        Clear paint from the given instructions.

        Internal routine to force called action to the main thread.
        """
        bv = disassembler.bv
        for address in instructions:
            for func in bv.get_functions_containing(address):
                func.set_auto_instr_highlight(address, HighlightStandardColor.NoHighlightColor)
        self._painted_instructions -= set(instructions)
        self._action_complete.set()

    def _paint_nodes(self, nodes_coverage):
        """
        Paint node level coverage defined by the current database mappings.

        Internal routine to force called action to the main thread.
        """
        bv = disassembler.bv
        color = HighlightStandardColor.BlueHighlightColor
        for node_coverage in nodes_coverage:
            node_metadata = node_coverage._database._metadata.nodes[node_coverage.address]

            # TODO/BINJA: change to containing??
            for node in bv.get_basic_blocks_starting_at(node_metadata.address):
                node.highlight = color

            self._painted_nodes.add(node_metadata.address)
        self._action_complete.set()

    def _clear_nodes(self, nodes_metadata):
        """
        Clear paint from the given graph nodes.

        Internal routine to force called action to the main thread.
        """
        bv = disassembler.bv
        for node_metadata in nodes_metadata:

            # TODO/BINJA: change to containing??
            for node in bv.get_basic_blocks_starting_at(node_metadata.address):
                node.highlight = HighlightStandardColor.NoHighlightColor

            self._painted_nodes.discard(node_metadata.address)
        self._action_complete.set()

    def _cancel_action(self, job):
        pass # TODO/BINJA

    #------------------------------------------------------------------------------
    # Painting - Functions
    #------------------------------------------------------------------------------

    def _paint_function(self, address):
        """
        Paint function instructions & nodes with the current database mappings.
        """
        return # TODO/BINJA

    #------------------------------------------------------------------------------
    # Priority Painting
    #------------------------------------------------------------------------------

    def _priority_paint(self):
        """
        Immediately repaint regions of the database visible to the user.
        """
        return True # TODO/BINJA
