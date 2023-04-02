from asciicast.cast import Cast


cast = Cast(typing_delay=0.03)

cast.echo("# How to use asciicast?")
cast.wait(0.5)

cast.echo("# You first need to write a script for your video.")
cast.wait(0.2)

cast.echo("# It could look something like this:")
cast.wait(0.2)

cast.type("cat -n examples/demo1.py")
cast.wait(0.2)

cast.echo("# Now you can use asciicast to generate cast file.")

cast.echo("# That is it. Don't rerecord your video because you did a typo or")
cast.echo("# typed to slow.")

cast.run()
