import sys

from bpy.props import EnumProperty, BoolProperty, FloatProperty, StringProperty
from bpy.types import PropertyGroup

mesh_triangle_types_items = (
    ('NORMAL', 'Normal', 'Normal one-sided', 0),
    ('NORMAL_TWO_SIDED', 'Normal Two-Sided', 'Normal but two-sided', 1),
    ('TRANSLUCENT', 'Translucent', 'Translucent two-sided', 2),
    ('MASKED', 'Masked', 'Masked two-sided', 3),
    ('MODULATE', 'Modulate', 'Modulation blended two-sided', 4),
    ('PLACEHOLDER', 'Placeholder', 'Placeholder triangle for positioning weapon. Invisible', 8),
)

mesh_triangle_bit_flags_items = (
    ('UNLIT', 'Unlit', 'Full brightness, no lighting', 16),
    ('FLAT', 'Flat', 'Flat surface, don\'t do bMeshCurvy thing', 32),
    ('ENVIRONMENT', 'Environment', 'Environment mapped', 64),
    ('NO_SMOOTH', 'No Smooth', 'No bilinear filtering on this poly\'s texture', 128),
)

class PSX_PG_material(PropertyGroup):
    mesh_triangle_type: EnumProperty(items=mesh_triangle_types_items, name='Triangle Type')
    mesh_triangle_bit_flags: EnumProperty(items=mesh_triangle_bit_flags_items, name='Triangle Bit Flags',
                                          options={'ENUM_FLAG'})

mesh_triangle_types_items_dict = {item[0]: item[3] for item in mesh_triangle_types_items}
mesh_triangle_bit_flags_items_dict = {item[0]: item[3] for item in mesh_triangle_bit_flags_items}


def triangle_type_and_bit_flags_to_poly_flags(mesh_triangle_type: str, mesh_triangle_bit_flags: set[str]) -> int:
    poly_flags = 0
    poly_flags |= mesh_triangle_types_items_dict.get(mesh_triangle_type, 0)
    for flag in mesh_triangle_bit_flags:
        poly_flags |= mesh_triangle_bit_flags_items_dict.get(flag, 0)
    return poly_flags


def poly_flags_to_triangle_type_and_bit_flags(poly_flags: int) -> (str, set[str]):
    try:
        triangle_type = next(item[0] for item in mesh_triangle_types_items if item[3] == (poly_flags & 15))
    except StopIteration:
        triangle_type = 'NORMAL'
    triangle_bit_flags = {item[0] for item in mesh_triangle_bit_flags_items if item[3] & poly_flags}
    return triangle_type, triangle_bit_flags

empty_set = set()


def should_import_mesh_get(self):
    return self.import_components in {'ALL', 'MESH'}

def should_import_skleton_get(self):
    return self.import_components in {'ALL', 'SKELETON'}


class PskImportMixin:
    should_import_vertex_colors: BoolProperty(
        default=True,
        options=empty_set,
        name='Import Vertex Colors',
        description='Import vertex colors, if available'
    )
    vertex_color_space: EnumProperty(
        name='Vertex Color Space',
        options=empty_set,
        description='The source vertex color space',
        default='SRGBA',
        items=(
            ('LINEAR', 'Linear', ''),
            ('SRGBA', 'sRGBA', ''),
        )
    )
    should_import_vertex_normals: BoolProperty(
        default=True,
        name='Import Vertex Normals',
        options=empty_set,
        description='Import vertex normals, if available'
    )
    should_import_extra_uvs: BoolProperty(
        default=True,
        name='Import Extra UVs',
        options=empty_set,
        description='Import extra UV maps, if available'
    )
    import_components: EnumProperty(
        name='Import Components',
        options=empty_set,
        description='Determine which components to import',
        items=(
            ('ALL', 'Mesh & Skeleton', 'Import mesh and skeleton'),
            ('MESH', 'Mesh Only', 'Import mesh only'),
            ('SKELETON', 'Skeleton Only', 'Import skeleton only'),
        ),
        default='ALL'
    )
    should_import_mesh: BoolProperty(
        name='Import Mesh',
        get=should_import_mesh_get,
    )
    should_import_materials: BoolProperty(
        default=True,
        name='Import Materials',
        options=empty_set,
    )
    should_import_skeleton: BoolProperty(
        name='Import Skeleton',
        get=should_import_skleton_get,
    )
    bone_length: FloatProperty(
        default=1.0,
        min=sys.float_info.epsilon,
        step=100,
        soft_min=1.0,
        name='Bone Length',
        options=empty_set,
        subtype='DISTANCE',
        description='Length of the bones'
    )
    should_import_shape_keys: BoolProperty(
        default=True,
        name='Import Shape Keys',
        options=empty_set,
        description='Import shape keys, if available'
    )
    scale: FloatProperty(
        name='Scale',
        default=1.0,
        soft_min=0.0,
    )
    bdk_repository_id: StringProperty(
        name='BDK Repository ID',
        default='',
        options=empty_set,
        description='The ID of the BDK repository to use for loading materials'
    )


classes = (
    PSX_PG_material,
)
