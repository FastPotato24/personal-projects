import game.mechanics as game
import game.interface as ui

dummy = game.Entity("dummy", **{"meta": {"name": "Test", "description": "This is a test entity."}})
test = ui.Interface(dummy)