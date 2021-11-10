from prmexporter.pipeline.main import main


def test_main_returns_one():

    actual = main()

    assert actual == 1
