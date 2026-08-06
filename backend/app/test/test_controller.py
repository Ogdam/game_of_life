from engine.controller import Controller


def test_set_size_resizes_underlying_game():
    controller = Controller(height=10, width=10)

    controller.set_size(height=20, width=30)

    assert controller.game.height == 20
    assert controller.game.width == 30


def test_get_speed_returns_current_speed():
    controller = Controller()
    controller.set_speed(3)

    assert controller.get_speed() == 3
