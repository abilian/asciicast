from asciicast.cast import Cast


def test_cast():
    cast = Cast()
    cast.echo("# How to use asciicast?")
    cast.wait(1.0)
    cast.type("echo test")
    cast.run()
