from mazegen import MazeGenerator
generator = MazeGenerator(width=5, height=5, perfect=True)
maze = generator.generate()
print(f"Success! Generated a {maze.width}x{maze.height} maze from an external project!")
