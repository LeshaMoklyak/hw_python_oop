from dataclasses import dataclass
from typing import Type, List


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = ('Тип тренировки: {training_type};'
                    " Длительность: {duration:.3f} ч.;"
                    ' Дистанция: {distance:.3f} км;'
                    ' Ср. скорость: {speed:.3f} км/ч;'
                    ' Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(training_type=self.training_type,
                                   duration=self.duration,
                                   distance=self.distance,
                                   speed=self.speed,
                                   calories=self.calories)


class Training:
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_H: float = 60
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        raise NotImplementedError(
            'Данный метод класса {} не реализован'.format(type(self).__name__)
        )

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration
                * self.MIN_IN_H)


class SportsWalking(Training):
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: float = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + ((self.get_mean_speed() * self.KMH_IN_MSEC) ** 2 / (
                    self.height / self.CM_IN_M))
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                * self.duration * self.MIN_IN_H)


class Swimming(Training):
    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_WEIGHT_MULTIPLIER: float = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration
                )

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                * self.duration)


DATA_TRAININGS: dict[str, Type[Training]] = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking}


def read_package(workout_type: str,
                 data: List[int],
                 ) -> Training:
    return DATA_TRAININGS[workout_type](*data)


def main(training: Training) -> None:
    info = training.show_training_info()
    message = info.get_message()
    print(message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
