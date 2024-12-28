import game.mechanics as game
import game.interface as ui

test = game.Entity("dummy", **{"meta": {"name": "Test", "description": "This is a test entity."}})
print(test.data)