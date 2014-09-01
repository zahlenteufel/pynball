import pygame, sys, math, time
from vector import vector
from segment import segment
from ball import ball
from finger import left_finger, right_finger

BLACK = (0, 0, 0)
DARK_GREEN = (128, 255, 0)

class pynball:

	WIDTH = 400
	HEIGHT = 600
	FPS = 40

	def __init__(self):
		pygame.init()

		self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), 0, 32)
		self.clock = pygame.time.Clock()

		exterior_walls = [
			segment(vector(-1, -1), vector(-1, self.HEIGHT), DARK_GREEN),
			segment(vector(-1, -1), vector(self.WIDTH, -1), DARK_GREEN),
			segment(vector(self.WIDTH, -1), vector(self.WIDTH, self.HEIGHT), DARK_GREEN),
			segment(vector(self.WIDTH, self.HEIGHT), vector(-1, self.HEIGHT), DARK_GREEN)
			]

		obstacles = [
			segment(vector(50, 460), vector(140, 540), DARK_GREEN),
			segment(vector(260, 540), vector(320, 485), DARK_GREEN)
			]

		self.segments = exterior_walls + obstacles

		self.left_finger = left_finger(vector(140, 540), 40, -math.pi / 4, math.pi / 3)
		self.right_finger = right_finger(vector(260, 540), 40, -math.pi / 4, math.pi / 3)

		self.ball = ball(vector(200, 200), 10, vector(0, 0))

		pygame.display.set_caption("Pynball")

		self.game_loop()

	def left(self):
		self.left_finger.trigger()

	def right(self):
		self.right_finger.trigger()

	def process_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT or \
				event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_z:
					self.left()
				elif event.key == pygame.K_m:
					self.right()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				self.ball.center = vector(pos[0], pos[1])

	def draw(self, screen):
		screen.fill(BLACK)

		for segment in self.segments:
			segment.draw(screen)

		self.left_finger.segment().draw(screen)
		self.right_finger.segment().draw(screen)

		self.ball.draw(screen)

	def game_loop(self):
		while True:
			self.process_events()

			for i in xrange(10):
				self.ball.apply_gravity()
				self.left_finger.update_move()
				self.right_finger.update_move()

				self.ball.apply_colissions(
					self.segments + [
					self.left_finger.segment(),
					self.right_finger.segment()])

			self.draw(self.screen)
			pygame.display.flip()

			self.clock.tick(self.FPS)


if __name__ == "__main__":
	pynball = pynball()
