"""List of choices to be used in selections"""

MALE = 'm'
FEMALE = 'f'
UNKNOWN = 'u'
SMALL = 's'
MEDIUM = 'm'
LARGE = 'l'
XLARGE = 'xl'
LIKED = 'l'
DISLIKED = 'd'
BABY = 'b'
YOUNG = 'y'
ADULT = 'a'
SENIOR = 's'


GENDERS = (
    (MALE, 'male'),
    (FEMALE, 'female'),
    (UNKNOWN, 'unknown')
)

SIZES = (
    (SMALL, 'small'),
    (MEDIUM, 'medium'),
    (LARGE, 'large'),
    (XLARGE, 'x-large'),
    (UNKNOWN, 'unknown')
)

STATUS = (
    (LIKED, 'like'),
    (DISLIKED, 'dislike'),
    (UNKNOWN, 'undecided')
)

AGE = (
    (BABY, 'baby'),
    (YOUNG, 'young'),
    (ADULT, 'adult'),
    (SENIOR, 'senior')
)