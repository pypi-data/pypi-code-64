# Created: 06.2020
# Copyright (c) 2020, Matthew Broadway
# Copyright (c) 2020, Manfred Moitzi
# License: MIT License
from typing import (
    TYPE_CHECKING, Dict, Optional, Tuple, Union, List, Iterable, Sequence, Set,
    cast,
)
import re
from ezdxf.entities import Attrib
from ezdxf.lldxf import const
from ezdxf.addons.drawing.type_hints import Color, RGB
from ezdxf.addons import acadctb
from ezdxf.sections.table import table_key as layer_key
from ezdxf.tools.rgb import luminance, DXF_DEFAULT_COLORS, int2rgb
from ezdxf.math import Vec2
from ezdxf.tools.pattern import scale_pattern

if TYPE_CHECKING:
    from ezdxf.eztypes import (
        DXFGraphic, Layout, Table, Layer, Linetype, Drawing, Textstyle, Vertex,
    )
    from ezdxf.entities.ltype import LinetypePattern

__all__ = [
    'Properties', 'LayerProperties', 'RenderContext', 'layer_key', 'rgb_to_hex',
    'hex_to_rgb', 'MODEL_SPACE_BG_COLOR', 'PAPER_SPACE_BG_COLOR',
    'compile_line_pattern', 'VIEWPORT_COLOR', 'CONTINUOUS_PATTERN',
    'set_color_alpha',
]

table_key = layer_key
MODEL_SPACE_BG_COLOR = '#212830'
PAPER_SPACE_BG_COLOR = '#ffffff'
VIEWPORT_COLOR = '#aaaaaa'  # arbitrary choice
CONTINUOUS_PATTERN = tuple()
SHX_FONTS = {
    # See examples in: CADKitSamples/Shapefont.dxf
    # Shape file structure is not documented, therefore replace this fonts by
    # true type fonts.
    # `None` is for: use the default font.
    'AMGDT': None,  # Tolerance symbols
    'AMGDT.SHX': None,
    'COMPLEX': None,
    'COMPLEX.SHX': None,
    'ISOCP': None,
    'ISOCP.SHX': None,
    'ITALIC': None,
    'ITALIC.SHX': None,
    'GOTHICG': None,
    'GOTHICG.SHX': None,
    'GREEKC': None,
    'GREEKC.SHX': None,
    'ROMANS': None,
    'ROMANS.SHX': None,
    'SCRIPTS': None,
    'SCRIPTS.SHX': None,
    'SCRIPTC': None,
    'SCRIPTC.SHX': None,
    'SIMPLEX': None,
    'SIMPLEX.SHX': None,
    'SYMATH': None,
    'SYMATH.SHX': None,
    'TXT': None,  # Default AutoCAD font
    'TXT.SHX': None,
}


def is_dark_color(color: Color, dark: float = 0.2) -> bool:
    luma = luminance(hex_to_rgb(color))
    return luma <= dark


class HatchPatternLine:
    # Similar ot hatch.PatternLine, but line pattern are stored as
    # simplified linetype pattern.
    def __init__(self, angle=0.0, base_point: 'Vertex' = (0, 0),
                 offset: 'Vertex' = (0, 0), pattern: Iterable[float] = None):
        self.angle: float = float(angle)  # in degrees
        self.base_point = Vec2(base_point)
        self.offset = Vec2(offset)
        # Same data format as linetype pattern:
        self.pattern: Tuple[float, ...] = tuple(pattern) \
            if pattern else CONTINUOUS_PATTERN


class Filling:
    SOLID = 0
    PATTERN = 1
    GRADIENT = 2

    def __init__(self):
        # Solid fill color is stored in Properties.color attribute
        self.type = Filling.SOLID
        # Gradient- or pattern name
        self.name: str = 'SOLID'
        # Gradient- or pattern angle
        self.angle: float = 0.0  # in degrees
        self.gradient_color1: Optional[Color] = None
        self.gradient_color2: Optional[Color] = None
        self.gradient_centered: float = 0.0  # todo: what's the meaning?
        self.pattern_scale: float = 1.0
        self.pattern: Sequence[HatchPatternLine] = []


class Properties:
    """ An implementation agnostic representation of entity properties like
    color and linetype.
    """

    def __init__(self):
        self.color: str = '#ffffff'  # format #RRGGBB or #RRGGBBAA
        # Color names should be resolved into a actual color value

        # Store linetype name for backends which don't have the ability to use
        # user-defined linetypes, but have some predefined linetypes, maybe
        # matching most common AutoCAD linetypes is possible.
        # Store linetype names in UPPERCASE.
        self.linetype_name: str = 'CONTINUOUS'

        # Linetypes: Complex DXF linetypes are not supported:
        # 1. Don't know if there are any backends which can use linetypes
        #    including text or shapes
        # 2. No decoder for SHX files available, which are the source for
        #    shapes in linetypes
        # 3. SHX files are copyrighted - including in ezdxf not possible
        #
        # Simplified DXF linetype definition:
        # all line elements >= 0.0, 0.0 = point
        # all gap elements > 0.0
        # Usage as alternating line - gap sequence: line-gap-line-gap ....
        # (line could be a point 0.0), line-line or gap-gap - makes no sense
        # Examples:
        # DXF: ("DASHED", "Dashed __ __ __ __ __ __ __ __ __ __ __ __ __ _",
        #      [0.6, 0.5, -0.1])
        # first entry 0.6 is the total pattern length = sum(linetype_pattern)
        # linetype_pattern: [0.5, 0.1] = line-gap
        # DXF: ("DASHDOTX2", "Dash dot (2x) ____  .  ____  .  ____  .  ____",
        #      [2.4, 2.0, -0.2, 0.0, -0.2])
        # linetype_pattern: [2.0, 0.2, 0.0, 0.2] = line-gap-point-gap
        # Stored as tuple, so pattern could be used as key for caching.
        # SVG dash-pattern does not support points, so a minimal line length
        # (maybe inferred from linewidth?) has to be used, which may alter the
        # overall line appearance - but linetype mapping will never be perfect.
        # The continuous pattern is an empty tuple ()
        self.linetype_pattern: Tuple[float, ...] = CONTINUOUS_PATTERN
        self.linetype_scale: float = 1.0
        # line weight in mm, todo: default lineweight is 0.25?
        self.lineweight: float = 0.25
        self.is_visible = True

        # The 'layer' attribute stores the resolved layer of an entity:
        # Entities inside of a block references get properties from the layer
        # of the INSERT entity, if they reside on the layer '0'.
        # To get the "real" layer of an entity, you have to use `entity.dxf.layer`
        self.layer: str = '0'

        # Font name for text entities, `None` is for the default font
        self.font: Optional[str] = None

        # Filling properties: Solid, Pattern, Gradient
        self.filling: Optional[Filling] = None

    def __str__(self):
        return f'({self.color}, {self.linetype_name}, {self.lineweight}, ' \
               f'"{self.layer}")'

    @property
    def rgb(self) -> RGB:
        """ Returns color as RGB tuple."""
        return hex_to_rgb(self.color[:7])  # ignore alpha if present

    @property
    def luminance(self) -> float:
        """ Returns perceived color luminance in range [0, 1] from dark to light.
        """
        return luminance(self.rgb)


class LayerProperties(Properties):
    """ Modified attribute meaning:

        is_visible: Whether entities belonging to this layer should be drawn
        layer: Stores real layer name (mixed case)

    """

    def __init__(self):
        super().__init__()
        self.has_aci_color_7 = False

    def get_entity_color_from_layer(self, fg: Color) -> Color:
        """ Returns the layer color or if layer color is ACI color 7 the
        given layout default foreground color `fg`.
        """
        if self.has_aci_color_7:
            return fg
        else:
            return self.color


DEFAULT_LAYER_PROPERTIES = LayerProperties()


class LayoutProperties:
    # The LAYOUT, BLOCK and BLOCK_RECORD entities do not have
    # explicit graphic properties.
    def __init__(self):
        self.name: str = 'Model'  # tab/display name
        self.units = 0  # default is unit less
        self._background_color: Color = MODEL_SPACE_BG_COLOR
        self._default_color: Color = '#ffffff'
        self._has_dark_background: bool = True

    @property
    def background_color(self) -> Color:
        """ Returns the default layout background color. """
        return self._background_color

    @property
    def default_color(self) -> Color:
        """ Returns the default layout foreground color. """
        return self._default_color

    @property
    def has_dark_background(self) -> bool:
        """ Returns ``True`` if the actual background-color is "dark". """
        return self._has_dark_background

    def set_layout(self, layout: 'Layout', bg: Optional[Color] = None,
                   fg: Optional[Color] = None,
                   units: Optional[int] = None) -> None:
        """ Setup default layout properties. """
        self.name = layout.name
        if bg is None:
            if self.name == 'Model':
                bg = MODEL_SPACE_BG_COLOR
            else:
                bg = PAPER_SPACE_BG_COLOR
        self.set_colors(bg, fg)
        if units is None:
            self.units = layout.units
        else:
            self.units = int(units)

    def set_colors(self, bg: Color, fg: Color = None) -> None:
        """ Setup default layout colors.

        Required color format "#RRGGBB" or including alpha transparency
        "#RRGGBBAA".
        """
        if not is_valid_color(bg):
            raise ValueError(f'Invalid background color: {bg}')
        self._background_color = bg
        if len(bg) == 9:  # including transparency
            bg = bg[:7]
        self._has_dark_background = is_dark_color(bg)
        if fg is not None:
            if not is_valid_color(fg):
                raise ValueError(f'Invalid foreground color: {fg}')
            self._default_color = fg
        else:
            self._default_color = '#ffffff' if self._has_dark_background \
                else '#000000'


class RenderContext:
    def __init__(self, doc: Optional['Drawing'] = None, *, ctb: str = '',
                 export_mode: bool = False):
        """ Represents the render context for the DXF document `doc`.
        A given `ctb` file (plot style file)  overrides the default properties.

        Args:
            doc: The document that is being drawn
            ctb: A path to a plot style table to use
            export_mode: Whether to render the document as it would look when
                exported (plotted) by a CAD application to a file such as pdf,
                or whether to render the document as it would appear inside a
                CAD application.
        """
        self._saved_states: List[Properties] = []
        self.line_pattern = _load_line_pattern(doc.linetypes) if doc else dict()
        self.current_layout = LayoutProperties()  # default is 'Model'
        self.current_block_reference: Optional[Properties] = None
        self.plot_styles = self._load_plot_style_table(ctb)
        self.export_mode = export_mode
        # Always consider: entity layer may not exist
        # Layer name as key is normalized, most likely name.lower(), but may
        # change in the future.
        self.layers: Dict[str, LayerProperties] = dict()
        # Text-style -> font mapping
        self.fonts: Dict[str, str] = dict()
        self.units = 0  # store modelspace units as enum, see ezdxf/units.py
        self.linetype_scale: float = 1.0  # overall modelspace linetype scaling
        if doc:
            self._setup_layers(doc)
            self._setup_text_styles(doc)
            self.linetype_scale = doc.header.get('$LTSCALE', 1.0)
            self.units = doc.header.get('$INSUNITS', 0)
            if self.units == 0:
                # set default units based on measurement system:
                # imperial (0) / metric (1)
                if doc.header.get('$MEASUREMENT', 1) == 1:
                    self.units = 6  # 1 m
                else:
                    self.units = 1  # 1 in
        self.current_layout.units = self.units
        self._hatch_pattern_cache: Dict[
            str, Sequence[HatchPatternLine]] = dict()

    def _setup_layers(self, doc: 'Drawing'):
        for layer in doc.layers:  # type: Layer
            self.add_layer(layer)

    def _setup_text_styles(self, doc: 'Drawing'):
        for text_style in doc.styles:  # type: Textstyle
            self.add_text_style(text_style)

    def add_layer(self, layer: 'Layer') -> None:
        """ Setup layer properties. """
        properties = LayerProperties()
        name = layer_key(layer.dxf.name)
        # Store real layer name (mixed case):
        properties.layer = layer.dxf.name
        properties.color = self._true_layer_color(layer)

        # Depend layer ACI color from layout background color?
        # True color overrides ACI color and layers with only true color set
        # have default ACI color 7!
        if not layer.has_dxf_attrib('true_color'):
            properties.has_aci_color_7 = layer.dxf.color == 7

        # Normalize linetype names to UPPERCASE:
        properties.linetype_name = str(layer.dxf.linetype).upper()
        properties.linetype_pattern = self.line_pattern.get(
            properties.linetype_name, CONTINUOUS_PATTERN)
        properties.lineweight = self._true_layer_lineweight(
            layer.dxf.lineweight)
        properties.is_visible = layer.is_on() and not layer.is_frozen()
        if self.export_mode:
            properties.is_visible &= bool(layer.dxf.plot)
        self.layers[name] = properties

    def add_text_style(self, text_style: 'Textstyle'):
        """ Setup text style properties. """
        name = table_key(text_style.dxf.name)
        font = text_style.dxf.font

        # Map SHX fonts to True Type Fonts:
        if font.upper() in SHX_FONTS:
            font = SHX_FONTS[font.upper()]
        self.fonts[name] = font

    def _true_layer_color(self, layer: 'Layer') -> Color:
        if layer.dxf.hasattr('true_color'):
            return rgb_to_hex(layer.rgb)
        else:
            # Don't use layer.dxf.color: color < 0 is layer state off
            aci = layer.color
            # aci: 0=BYBLOCK, 256=BYLAYER, 257=BYOBJECT
            if aci < 1 or aci > 255:
                aci = 7  # default layer color
            return self._aci_to_true_color(aci)

    def _true_layer_lineweight(self, lineweight: int) -> float:
        if lineweight < 0:
            return self.default_lineweight()
        else:
            return float(lineweight) / 100.0

    @staticmethod
    def _load_plot_style_table(filename: str):
        # Each layout can have a different plot style table stored in
        # Layout.dxf.current_style_sheet.
        # HEADER var $STYLESHEET stores the default ctb-file name.
        try:
            ctb = acadctb.load(filename)
        except IOError:
            ctb = acadctb.new_ctb()

        # Colors in CTB files can be RGB colors but don't have to,
        # therefore initialize color without RGB values by the
        # default AutoCAD palette:
        for aci in range(1, 256):
            entry = ctb[aci]
            if entry.has_object_color():
                # initialize with default AutoCAD palette
                entry.color = int2rgb(DXF_DEFAULT_COLORS[aci])
        return ctb

    def set_layers_state(self, layers: Set[str], state=True):
        """ Set layer state of `layers` to on/off.

        Args:
             layers: set of layer names
             state: `True` turn this `layers` on and others off,
                    `False` turn this `layers` off and others on
        """
        layers = {layer_key(name) for name in layers}
        for name, layer in self.layers.items():
            if name in layers:
                layer.is_visible = state
            else:
                layer.is_visible = not state

    def set_current_layout(self, layout: 'Layout'):
        self.current_layout.set_layout(layout, units=self.units)

    @property
    def inside_block_reference(self) -> bool:
        """ Returns ``True`` if current processing state is inside of a block
        reference (INSERT).
        """
        return bool(self.current_block_reference)

    def push_state(self, block_reference: Properties) -> None:
        self._saved_states.append(self.current_block_reference)
        self.current_block_reference = block_reference

    def pop_state(self) -> None:
        self.current_block_reference = self._saved_states.pop()

    def resolve_all(self, entity: 'DXFGraphic') -> Properties:
        """ Resolve all properties of `entity`. """
        p = Properties()
        p.layer = self.resolve_layer(entity)
        resolved_layer = layer_key(p.layer)

        p.color = self.resolve_color(entity, resolved_layer=resolved_layer)
        p.linetype_name, p.linetype_pattern = \
            self.resolve_linetype(entity, resolved_layer=resolved_layer)
        p.lineweight = self.resolve_lineweight(entity,
                                               resolved_layer=resolved_layer)
        dxf = entity.dxf
        p.linetype_scale = dxf.ltscale
        p.is_visible = self.resolve_visible(entity,
                                            resolved_layer=resolved_layer)

        if dxf.hasattr('style'):
            p.font = self.resolve_font(entity)
        if entity.dxftype() == 'HATCH':
            p.filling = self.resolve_filling(entity)
        return p

    def resolve_visible(self, entity: 'DXFGraphic', *,
                        resolved_layer: Optional[str] = None) -> bool:
        """ Resolve the visibility state of `entity`.
        Returns ``True`` if `entity` is visible.
        """
        entity_layer = resolved_layer or layer_key(self.resolve_layer(entity))
        layer_properties = self.layers.get(entity_layer)
        if layer_properties and not layer_properties.is_visible:
            return False
        elif entity.dxftype() == 'ATTRIB':
            return (not bool(entity.dxf.invisible) and
                    not cast(Attrib, entity).is_invisible)
        else:
            return not bool(entity.dxf.invisible)

    def resolve_layer(self, entity: 'DXFGraphic') -> str:
        """ Resolve the layer of `entity`, this is only relevant for entities
        inside of block references.
        """
        layer = entity.dxf.layer
        if layer == '0' and self.inside_block_reference:
            layer = self.current_block_reference.layer
        return layer

    def resolve_color(self, entity: 'DXFGraphic', *,
                      resolved_layer: Optional[str] = None) -> Color:
        """ Resolve the rgb-color of `entity` as hex color string:
        "#RRGGBB" or "#RRGGBBAA".
        """
        aci = entity.dxf.color  # defaults to BYLAYER
        if aci == const.BYLAYER:
            entity_layer = resolved_layer or layer_key(
                self.resolve_layer(entity))
            layer = self.layers.get(
                entity_layer, DEFAULT_LAYER_PROPERTIES)
            color = layer.get_entity_color_from_layer(
                self.current_layout.default_color)
        elif aci == const.BYBLOCK:
            if not self.inside_block_reference:
                color = self.current_layout.default_color
            else:
                color = self.current_block_reference.color

        else:  # BYOBJECT
            color = self._true_entity_color(entity.rgb, aci)

        alpha = int(round((1.0 - entity.transparency) * 255))
        if alpha == 255:
            return color
        else:
            return set_color_alpha(color, alpha)

    def _true_entity_color(self,
                           true_color: Optional[Tuple[int, int, int]],
                           aci: int) -> Color:
        """ Returns rgb color in hex format: "#RRGGBB".

        `true_color` has higher priority than `aci`.
        """
        if true_color is not None:
            return rgb_to_hex(true_color)
        elif 0 < aci < 256:
            return self._aci_to_true_color(aci)
        else:
            return self.current_layout.default_color  # unknown / invalid

    def _aci_to_true_color(self, aci: int) -> Color:
        """ Returns the `aci` value (AutoCAD Color Index) as rgb value in
        hex format: "#RRGGBB".
        """
        if aci == 7:  # black/white; todo: this bypasses the plot style table
            if self.current_layout.has_dark_background:
                return '#ffffff'
            else:
                return '#000000'
        else:
            return rgb_to_hex(self.plot_styles[aci].color)

    def resolve_linetype(self, entity: 'DXFGraphic', *,
                         resolved_layer: str = None
                         ) -> Tuple[str, Tuple[float, ...]]:
        """ Resolve the linetype of `entity`. Returns a tuple of the linetype
        name as upper-case string and the simplified linetype pattern as tuple
        of floats.
        """
        aci = entity.dxf.color
        # Not sure if plotstyle table overrides actual entity setting?
        if (0 < aci < 256) and \
                self.plot_styles[aci].linetype != acadctb.OBJECT_LINETYPE:
            # todo: return special line types - overriding linetypes by
            #  plotstyle table
            pass
        name = entity.dxf.linetype.upper()  # default is 'BYLAYER'
        if name == 'BYLAYER':
            entity_layer = resolved_layer or layer_key(
                self.resolve_layer(entity))
            layer = self.layers.get(entity_layer, DEFAULT_LAYER_PROPERTIES)
            name = layer.linetype_name
            pattern = layer.linetype_pattern

        elif name == 'BYBLOCK':
            if self.inside_block_reference:
                name = self.current_block_reference.linetype_name
                pattern = self.current_block_reference.linetype_pattern
            else:
                # There is no default layout linetype
                name = 'STANDARD'
                pattern = CONTINUOUS_PATTERN
        else:
            pattern = self.line_pattern.get(name, CONTINUOUS_PATTERN)
        return name, pattern

    def resolve_lineweight(self, entity: 'DXFGraphic', *,
                           resolved_layer: str = None) -> float:
        """ Resolve the lineweight of `entity` in mm.

        DXF stores the lineweight in mm times 100 (e.g. 0.13mm = 13).
        The smallest line weight is 0 and the biggest line weight is 211.
        The DXF/DWG format is limited to a fixed value table,
        see: :attr:`ezdxf.lldxf.const.VALID_DXF_LINEWEIGHTS`

        CAD applications draw lineweight 0mm as an undefined small value, to
        prevent backends to draw nothing for lineweight 0mm the smallest
        return value is 0.01mm.

        """

        def lineweight():
            aci = entity.dxf.color
            # Not sure if plotstyle table overrides actual entity setting?
            if (0 < aci < 256) and self.plot_styles[
                aci].lineweight != acadctb.OBJECT_LINEWEIGHT:
                # overriding lineweight by plotstyle table
                return self.plot_styles.get_lineweight(aci)
            lineweight = entity.dxf.lineweight  # default is BYLAYER
            if lineweight == const.LINEWEIGHT_BYLAYER:
                entity_layer = resolved_layer or layer_key(
                    self.resolve_layer(entity))
                return self.layers.get(entity_layer,
                                       DEFAULT_LAYER_PROPERTIES).lineweight

            elif lineweight == const.LINEWEIGHT_BYBLOCK:
                if self.inside_block_reference:
                    return self.current_block_reference.lineweight
                else:
                    # There is no default layout lineweight
                    return self.default_lineweight()
            elif lineweight == const.LINEWEIGHT_DEFAULT:
                return self.default_lineweight()
            else:
                return float(lineweight) / 100.0

        return max(0.01, lineweight())

    def default_lineweight(self):
        """ Returns the default lineweight of the document. """
        # todo: is this value stored anywhere (e.g. HEADER section)?
        return 0.25

    def resolve_font(self, entity: 'DXFGraphic') -> Optional[str]:
        """ Resolve the text style of `entity` to a font name.
        Returns ``None`` for the default font.
        """
        if entity.dxf.hasattr('style'):
            return self.fonts.get(table_key(entity.dxf.style))
        else:
            return None

    def resolve_filling(self, entity: 'DXFGraphic') -> Optional[Filling]:
        """ Resolve filling properties (SOLID, GRADIENT, PATTERN) of `entity`.
        """

        def setup_gradient():
            filling.type = Filling.GRADIENT
            filling.name = gradient.name.upper()
            # todo: no idea when to use aci1 and aci2
            filling.color1 = rgb_to_hex(gradient.color1)
            if gradient.one_color:
                c = round(gradient.tint * 255)  # channel value
                filling.color2 = rgb_to_hex((c, c, c))
            else:
                filling.color2 = rgb_to_hex(gradient.color2)

            filling.angle = gradient.rotation
            filling.gradient_centered = gradient.centered

        def setup_pattern():
            filling.type = Filling.PATTERN
            filling.name = hatch.dxf.pattern_name.upper()
            filling.pattern_scale = hatch.dxf.pattern_scale
            filling.angle = hatch.dxf.pattern_angle
            if hatch.dxf.pattern_double:
                # This value is not editable by CAD-App-GUI:
                filling.pattern_scale *= 2  # todo: is this correct?

            filling.pattern = self._hatch_pattern_cache.get(filling.name)
            if filling.pattern:
                return

            pattern = hatch.pattern
            if not pattern:
                return

            # DXF stores the hatch pattern already rotated and scaled,
            # pattern_scale and pattern_rotation are just hints for the CAD
            # application to modify the pattern if required.
            # It's better to revert the scaling and rotation, because in general
            # back-ends do not handle pattern that way, they need a base-pattern
            # and separated scaling and rotation attributes and these
            # base-pattern could be cached by their name.
            base_pattern = scale_pattern(
                pattern.as_list(),
                1.0 / filling.pattern_scale,
                -filling.angle
            )
            simplified_pattern = []
            for angle, base_point, offset, dash_length_items in base_pattern:
                if len(dash_length_items) > 1:
                    line_pattern = compile_line_pattern(
                        None,
                        dash_length_items
                    )
                else:
                    line_pattern = CONTINUOUS_PATTERN
                simplified_pattern.append(
                    HatchPatternLine(angle, base_point, offset, line_pattern)
                )
            filling.pattern = simplified_pattern
            self._hatch_pattern_cache[filling.name] = filling.pattern

        if entity.dxftype() != 'HATCH':
            return None

        hatch = cast('Hatch', entity)
        filling = Filling()
        if hatch.dxf.solid_fill:
            gradient = hatch.gradient
            if gradient is None:
                filling.type = Filling.SOLID
            else:
                if gradient.kind == 0:  # Solid
                    filling.type = Filling.SOLID
                    filling.color1 = rgb_to_hex(gradient.color1)
                else:
                    setup_gradient()
        else:
            setup_pattern()
        return filling


COLOR_PATTERN = re.compile('#[0-9A-Fa-f]{6,8}')


def is_valid_color(color: Color) -> bool:
    if type(color) is not Color:
        raise TypeError(f'Invalid argument type: {type(color)}.')
    if len(color) in (7, 9):
        return bool(COLOR_PATTERN.fullmatch(color))
    return False


def rgb_to_hex(
        rgb: Union[Tuple[int, int, int], Tuple[float, float, float]]) -> Color:
    """ Returns color in hex format: "#RRGGBB". """
    assert all(0 <= x <= 255 for x in rgb), f'invalid RGB color: {rgb}'
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'


def hex_to_rgb(hex_string: Color) -> RGB:
    """ Returns hex string color as (r, g, b) tuple. """
    hex_string = hex_string.lstrip('#')
    assert len(hex_string) == 6
    r = int(hex_string[0:2], 16)
    g = int(hex_string[2:4], 16)
    b = int(hex_string[4:6], 16)
    return r, g, b


def set_color_alpha(color: Color, alpha: int) -> Color:
    """ Returns `color` including the new `alpha` channel in hex format:
    "#RRGGBBAA".

    Args:
        color: may be an RGB or RGBA hex color string
        alpha: the new alpha value (0-255)
    """
    assert color.startswith('#') and len(color) in (
        7, 9), f'invalid RGB color: "{color}"'
    assert 0 <= alpha < 256, f'alpha out of range: {alpha}'
    return f'{color[:7]}{alpha:02x}'


def _load_line_pattern(linetypes: 'Table') -> Dict[str, Tuple]:
    """ Load linetypes defined in a DXF document into  as dictionary,
    key is the upper case linetype name, value is the simplified line pattern,
    see :func:`compile_line_pattern`.
    """
    pattern = dict()
    for linetype in linetypes:  # type: Linetype
        name = linetype.dxf.name.upper()
        pattern[name] = _compile_line_pattern_from_tags(linetype.pattern_tags)
    return pattern


def _merge_dashes(elements: Sequence[float]) -> Iterable[float]:
    """ Merge multiple consecutive lines, gaps or points into a single element.
    """

    def sign(v):
        if v < 0:
            return -1
        elif v > 0:
            return +1
        return 0

    buffer = elements[0]
    prev_sign = sign(buffer)
    for e in elements[1:]:
        if sign(e) == prev_sign:
            buffer += e
        else:
            yield buffer
            buffer = e
            prev_sign = sign(e)
    yield buffer


def _compile_line_pattern_from_tags(
        pattern: 'LinetypePattern') -> Tuple[float, ...]:
    """ Returns the simplified dash-gap-dash... line pattern,
    a dash-length of 0 represents a point.
    """
    # complex line types with text and shapes are not supported
    if pattern.is_complex_type():
        return CONTINUOUS_PATTERN

    pattern_length = 0.0
    elements = []
    for tag in pattern.tags:
        if tag.code == 40:
            pattern_length = tag.value
        elif tag.code == 49:
            elements.append(tag.value)

    if len(elements) < 2:
        return CONTINUOUS_PATTERN
    return compile_line_pattern(pattern_length, elements)


def compile_line_pattern(
        total_length: Optional[float],
        elements: Sequence[float]) -> Tuple[float, ...]:
    """ Returns the simplified dash-gap-dash... line pattern,
    a dash-length of 0 represents a point.
    """
    elements = list(_merge_dashes(elements))
    if total_length is None:
        pass
    elif len(elements) < 2 or total_length <= 0.0:
        return CONTINUOUS_PATTERN

    sum_elements = sum(abs(e) for e in elements)
    if total_length and total_length > sum_elements:  # append a gap
        elements.append(sum_elements - total_length)

    if elements[0] < 0:  # start with a gap
        e = elements.pop(0)
        if elements[-1] < 0:  # extend last gap
            elements[-1] += e
        else:  # add last gap
            elements.append(e)
    # returns dash-gap-point
    # possible: dash-point or point-dash - ignore this yet
    # never: dash-dash or gap-gap or point-point
    return tuple(abs(e) for e in elements)
