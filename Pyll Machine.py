from ursina import *

app = Ursina()

# window.borderless = False
window.fullscreen = True

Arrow              = load_texture("oreo_blue_cursors/arrow.png")
BGTexture          = load_texture("TexturePacks/Default/BG.png")
moveTexture        = load_texture("TexturePacks/Default/MoveCell.png")
generatorTexture   = load_texture("TexturePacks/Default/GeneratorCell.png")
ccwRotatorTexture  = load_texture("TexturePacks/Default/CCWRotatorCell.png")
cwRotatorTexture   = load_texture("TexturePacks/Default/CWRotatorCell.png")
playButtonTexture  = load_texture("Assets/Play.png")
pauseButtonTexture = load_texture("Assets/Pause.png")

cell_pick = 1
rotation_pick = 0

cell_place_position = (0, 0)

camera.orthographic = True

pplace   = None
pdestroy = None

timee = 0
timeq = 0

def play():
    pass

def pause():
    pass

def reset():
    pass

def update():
    global rotation_pick, cell_pick
    global cells, cell
    global bg, BG
    global timee, timeq
    global show
    
    if held_keys['1']: cell_pick = 1
    if held_keys['2']: cell_pick = 2
    
    for i in show:
        i.color = "#a0a0a0"
    show[cell_pick-1].color = color.white
    
    if held_keys['e']:
        if timee == 0:
            rotation_pick = (rotation_pick + 1) % 4
            for i in show:
                i.rotation_z += 90
        timee = 1
    else:
        timee = 0
    
    if held_keys['q']:
        if timeq == 0:
            rotation_pick = (rotation_pick - 1) % 4
            for i in show:
                i.rotation_z -= 90
        timeq = 1
    else:
        timeq = 0
    
    if held_keys['left mouse']:
        global pplace
        hentity = mouse.hovered_entity
        
        if type(hentity) == BG or type(hentity) in cells:
            try:
                if type(hentity) != cells[cell_pick - 1] or hentity.rotation != (0, 0, 90 * rotation_pick):
                    if hentity != pplace:
                        placecell(hentity)
                        pplace = hentity
            except AssertionError as e:
                pass
    
    if held_keys['right mouse']:
        global pdestroy
        hentity = mouse.hovered_entity
        
        if type(hentity) in cells and hentity != pdestroy:
            destroycell(hentity)
            pdestroy = hentity
    
    camera.y += held_keys['w'] * 0.1
    camera.x -= held_keys['a'] * 0.1
    camera.y -= held_keys['s'] * 0.1
    camera.x += held_keys['d'] * 0.1
    
    camera.fov -= held_keys['x'] * 0.25
    camera.fov += held_keys['z'] * 0.25


mouse.visible = False
Cursor(origin = (-.34, .49), texture = Arrow, color = color.white, scale = (0.04, 0.04))

class BG(Entity):
    def __init__(self, position = (0, 0, 0)):
        super().__init__(
            model = "quad",
            collider = "box",
            texture = BGTexture,
            color = color.white,
            position = position,
        )

class MoveCell(Entity):
    def __init__(self, position = (0, 0, 0), rotation = (0, 0, 0)):
        super().__init__(
            model = "quad",
            collider = "box",
            texture = moveTexture,
            color = color.white,
            position = position,
            rotation = rotation,
        )

class GeneratorCell(Entity):
    def __init__(self, position = (0, 0, 0), rotation = (0, 0, 0)):
        super().__init__(
            model = "quad",
            collider = "box",
            texture = generatorTexture,
            color = color.white,
            position = position,
            rotation = rotation,
        )

def placecell(self):
    global rotation_pick, cell_pick, cells, cell
    cell = cells[cell_pick - 1](position = self.position, rotation = (0, 0, 90 * rotation_pick))
    destroy(self)

def destroycell(self):
    global bg
    bg = BG(position = self.position)
    destroy(self)

cells = [
    MoveCell,
    GeneratorCell,
    # CCWRotatorCell,
    # CWRotatorCell,
]

for x in range(10):
    for y in range(10):
        bg = BG((x - 4.5, y - 4.5, 0))

background = Entity(model = "quad",
                    scale = (10000, 10000, 0),
                    color = "#292929",
                    position = (0, 0, 10),
                    )

def pickCell(pick):
    global cell_pick
    cell_pick = pick

show = [
        Entity(parent = camera.ui,
               model = "quad",
               collider = "box",
               texture = moveTexture,
               scale = (0.1, 0.1),
               position = (-0.7, -0.4),
               color = color.white,
               on_click = Func(pickCell, 1),
               ),
        
        Entity(parent = camera.ui,
               model = "quad",
               collider = "box",
               texture = generatorTexture,
               scale = (0.1, 0.1),
               position = (-0.58, -0.4),
               color = "#a0a0a0",
               on_click = Func(pickCell, 2),
               ),
        ]

play = Button(parent = camera.ui,
               model = "quad",
               texture = playButtonTexture,
               scale = (0.1, 0.1),
               position = (-0.58, -0.4),
               on_click = play,
              )

app.run()
