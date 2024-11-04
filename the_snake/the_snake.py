from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Класс игрового объекта от которого будут наследоваться прочие объекты"""

    def __init__(self):
        self.position = None
        self.body_color = None

    def draw(self):
        """Рисуем..."""
        pass


class Apple (GameObject):
    """
    Класс, представляющий яблоко в игре.

    Яблоко имеет цвет и случайным образом изменяет свою позицию на игровом поле
    """

    def __init__(self):
        """Инициализирует экземпляр яблока, задаёт цвет и случайную позицию."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def draw(self, screen):
        """Рисует яблоко"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Задаёт случайную позицию для яблока"""
        self.position = (randint(0, (GRID_WIDTH - 1)) * GRID_SIZE,
                         randint(0, (GRID_HEIGHT - 1)) * GRID_SIZE)


class Snake (GameObject):
    """Класс представляющий змею в игре"""

    def __init__(self):
        super().__init__()
        self.positions = [
            ((SCREEN_WIDTH // 2 // GRID_SIZE * GRID_SIZE),
             (SCREEN_HEIGHT // 2 // GRID_SIZE * GRID_SIZE))
        ]
        self.body_color = SNAKE_COLOR
        self.last = self.positions[0]
        self.next_direction = None
        self.direction = RIGHT

    def draw(self, screen):
        """Рисует змею"""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Выполняет передвижение"""
        # Сохраняем текущий последний сегмент для затирания
        self.last = self.positions[-1]

        # Определяем новую позицию головы, добавляя к ней направление движения
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x * GRID_SIZE, head_y + dir_y * GRID_SIZE)

        # предел змейки
        if new_head[0] >= SCREEN_WIDTH:
            new_head = (0, new_head[1])

        elif new_head[1] >= SCREEN_HEIGHT:
            new_head = (new_head[0], 0)

        elif new_head[0] < 0:
            new_head = (SCREEN_WIDTH - GRID_SIZE, new_head[1])

        elif new_head[1] < 0:
            new_head = (new_head[0], SCREEN_HEIGHT - GRID_SIZE)

        # Вставляем новую голову в начало списка позиций
        self.positions = [new_head] + self.positions[:-1]

    def update_direction(self):
        """Обновляет направление движения змеи"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змеи"""
        return self.positions[0]

    def reset(self):
        """Сбрасывает игру на старт"""
        head = self.get_head_position()
        if head in self.positions[1:]:
            self.direction = RIGHT
            self.positions = [((SCREEN_WIDTH // 2 // GRID_SIZE * GRID_SIZE),
                               (SCREEN_HEIGHT // 2 // GRID_SIZE * GRID_SIZE))]


def check_collision(apple, snake):
    """Проверяет не съедено ли яблоко"""
    if snake.get_head_position() == apple.position:
        snake.positions.append(snake.last)
        apple.randomize_position()


def handle_keys(snake):
    """Проверяет нажатие игровых кнопок"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.direction = RIGHT


def main():
    """Игра запускается через эту функцию"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        screen.fill((0, 0, 0))
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        check_collision(apple, snake)
        snake.reset()
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()
        # Тут опишите основную логику игры.


if __name__ == '__main__':
    main()
