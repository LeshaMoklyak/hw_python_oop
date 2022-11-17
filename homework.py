class InfoMessage:
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        message = (f'Тип тренировки: { self.training_type};'
                   f" Длительность: { self.duration:.3f} ч.;"
                   f' Дистанция: { self.distance:.3f} км;'
                   f' Ср. скорость: { self.speed:.3f} км/ч;'
                   f' Потрачено ккал: { self.calories:.3f}.')
        return message


class Training:
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        length = self.action * self.LEN_STEP / self.M_IN_KM
        return length

    def get_mean_speed(self) -> float:
        avg_speed = self.get_distance() / self.duration
        return avg_speed

    def get_spent_calories(self) -> float:
        pass

    def show_training_info(self) -> InfoMessage:
        info = InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )
        return info


class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H)
      
        return calories


class SportsWalking(Training):
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                    + ((self.get_mean_speed()**2) // self.height)
                    * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.height)
                    * (self.duration * self.MIN_IN_H))
        return calories


class Swimming(Training):
    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_WEIGHT_MULTIPLIER: float = 2

    def __init__(self, action: int, duration: float, weight:
                 float, length_pool: float, count_pool) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        length = (self.length_pool * self.count_pool
                  / self.M_IN_KM / self.duration)
        return length

    def get_spent_calories(self) -> float:
        calories = ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.CALORIES_WEIGHT_MULTIPLIER * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    dict_training = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    """Прочитать данные полученные от датчиков."""
    return dict_training[workout_type](*data)


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
