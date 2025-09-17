import habitat
import tools
import enum
import chars
from functools import partial

def cap_at_100(num):
    return num <= 100

class DS_Constants: 
    REV_CHANNEL_SENTINEL = 'none' 
    REV_CHANNEL_KEY = 'rev_channel' 
    REV_INTERVAL_KEY = 'rev_interval' 
    REV_LAST_CHECKED_KEY = 'rev_last_checked' 

    DEFAULT_PREFIX = ',' 
    MAX_PREFIX = 5
    PREFIX_SENTINEL = 'remove' 

    INVITE_LINK = 'https://discord.com/oauth2/authorize?client_id=796151711571116042&permissions=347136&scope=bot' 
    EXAMPLE_USERNAME = 'iliekp_724' 
    EXAMPLE_PFP_URL = 'https://deeeep.io/files/379126.gif?1626117634391' 
    USERNAME_LOCATION = 'username location.PNG' 
    LINK_COPYING = 'link copying.PNG' 
    NOMBRE_CHANGE = 'nombre change.PNG' 
    TREE = 'evolution tree.png'

    SIGNING_IN = 'https://cdn.discordapp.com/attachments/493952969277046787/978961977349136394/signing_in.gif'
    OPENING_PROFILE = 'https://cdn.discordapp.com/attachments/493952969277046787/978961977957290024/opening_profile.gif'
    ADDING_DISCORD = 'https://cdn.discordapp.com/attachments/493952969277046787/978962850875834378/adding_discord.gif'
    CONNECT_COMMAND = 'https://cdn.discordapp.com/attachments/493952969277046787/978963699937194034/connect_command.gif'

    DATE_FORMAT = '%B %d, %Y' 
    REV_LOG_TIME_FORMAT = '%m-%d-%Y at %I:%M:%S %p' 
    MESSAGE_LOG_TIME_FORMAT = REV_LOG_TIME_FORMAT

    MAX_TITLE = 256
    MAX_DESC = 2048
    MAX_FIELD_VAL = 1024
    TRAIL_OFF = '...' 
    MAX_LOG = 1000000
    MAX_SEARCH_TIME = 60
    MAX_SKIN_SUGGESTIONS = 10

    OWNER_ID = 315682382147485697

    REQUEST_TIMEOUT = 15

    MENTION_REGEX = '\A<@!?(?P<member_id>[0-9]+)>\Z' 
    CHANNEL_REGEX = '\A<#(?P<channel_id>[0-9]+)>\Z' 

    DATA_URL_TEMPLATE = 'https://apibeta.deeeep.io/users/{}?ref=profile' 
    SOCIALS_URL_TEMPLATE = 'https://apibeta.deeeep.io/socialNetworks/u/{}'
    PFP_URL_TEMPLATE = 'https://cdn.deeeep.io/uploads/avatars/{}' 
    SERVER_LIST_URL = 'http://apibeta.deeeep.io/hosts?beta=1' 
    MAP_URL_TEMPLATE = 'https://apibeta.deeeep.io/maps/{}'
    APPROVED_SKINS_LIST_URL = 'https://apibeta.deeeep.io/skins?cat=all' 
    LOGIN_URL = 'https://apibeta.deeeep.io/auth/local/signin' 
    SKIN_BOARD_MEMBERS_URL = 'https://apibeta.deeeep.io/users/boardMembers' 
    LOGOUT_URL = 'https://api.deeeep.io/auth/logout' 
    PFP_REGEX = '\A(?:https?://)?(?:www\.)?deeeep\.io/files/(?P<acc_id>[0-9]+)(?:-temp)?\.[0-9A-Za-z]+(?:\?.*)?\Z' 
    USERNAME_REGEX = '\A@?(?P<username>.+)\Z' 
    USERNAME_SEARCH_TEMPLATE = 'https://apibeta.deeeep.io/users/u/{}' 
    PROFILE_TEMPLATE = 'https://apibeta.deeeep.io/users/u/{}?ref=profile'
    BETA_PFP_TEMPLATE = 'https://cdn.deeeep.io/uploads/avatars/{}'
    PROFILE_PAGE_TEMPLATE = 'https://beta.deeeep.io/u/{}'
    PROFILE_PAGE_REGEX = '\A(?:(?:https?:\/\/)beta\.deeeep\.io\/u\/)?(?P<username>[^\/.?]+)\Z'
    RANKINGS_TEMPLATE = 'https://apibeta.deeeep.io/userStats/{}'

    DEFAULT_PFP = 'https://deeeep.io/new/assets/placeholder.png' 
    DEFAULT_BETA_PFP = 'https://beta.deeeep.io/img/avatar.png'

    SKIN_ASSET_URL_TEMPLATE = 'https://deeeep.io/assets/skins/{}' 
    CUSTOM_SKIN_ASSET_URL_TEMPLATE = 'https://cdn.deeeep.io/custom/skins/{}'
    SKIN_URL_TEMPLATE = 'https://apibeta.deeeep.io/skins/{}' 
    SKIN_REVIEW_TEMPLATE = 'https://api.deeeep.io/skins/{}/review' 
    SKIN_STORE_PAGE_PREFIX = 'https://beta.deeeep.io/store/skins/'
    SKIN_STORE_PAGE_TEMPLATE = SKIN_STORE_PAGE_PREFIX + '{}'

    SKIN_CONTRIBS_TEMPLATE = 'https://apibeta.deeeep.io/skins/creator/{}'
    MAP_CONTRIBS_TEMPLATE = 'https://apibeta.deeeep.io/maps/u/{}?page=1&orderBy=updated_at&direction=DESC&period=0'
    EMOTE_CONTRIBS_TEMPLATE = 'https://apibeta.deeeep.io/emotes/creator/{}'
    PET_CONTRIBS_TEMPLATE = 'https://apibeta.deeeep.io/pets/creator/{}'

    CROWDL_NAME_TEMPLATE = 'https://api.crowdl.io/entries?project_id=1&key={}-name&lang=en'
    CROWDL_DESC_TEMPLATE = 'https://api.crowdl.io/entries?project_id=1&key={}-message&lang=en'

    STONKS_THRESHOLD = 150

    STAT_CHANGE_TRANSLATIONS = {
        'HM': 'healthMultiplier', 
        'DM': 'damageMultiplier', 
        'DB': 'damageBlock', 
        'DR': 'damageReflection', 
        'AP': 'armorPenetration', 
        'BR': 'bleedReduction', 
        'OT': 'oxygenTime', 
        'TT': 'temperatureTime', 
        'PT': 'pressureTime', 
        'ST': 'salinityTime', 
        'SS': 'sizeMultiplier', 
        'HA': 'habitat', 
    } 

    STAT_FORMATS = {
        'boosts': ('boosts', '{}'), 
        'level': ('tier', '{}', lambda num: num + 1), 
        'oxygenTime': ('oxygen time', '{} seconds'), 
        'temperatureTime': ('temperature time', '{} seconds'),
        'pressureTime': ('pressure time', '{} seconds'),
        'salinityTime': ('salinity time', '{} seconds'),
        'speedMultiplier': ('base speed', '{:.0%}'),
        'walkSpeedMultiplier': ('walk speed', '{:.0%}'),
        'sizeMultiplier': ('size scale', '{}x', lambda num: float(num)), 
        'sizeScale': ('dimensions', "{0[0]} width, {0[1]} height", lambda dims: (dims['x'] * 1.0, dims['y'] * 1.0)),
        'damageMultiplier': ('damage', '{} HP', lambda num: tools.trunc_float(num * 20)), 
        'healthMultiplier': ('health', '{} HP', lambda num: tools.trunc_float(num * 100)),
        'damageBlock': ('armor', '{}%', 100),
        'damageReflection': ('damage reflection', '{}%', 100), 
        'bleedReduction': ('bleed reduction', '{}%', 100), 
        'poisonResistance': ('poison resistance', '{}%', 100),
        'armorPenetration': ('armor penetration', '{}%', 100), 
        'habitat': ('habitat', '{}', lambda num: habitat.Habitat(num)), 
        'secondaryAbilityLoadTime': ('charged boost load time', '{} ms'), 
    }

    TYPE_REQUIREMENTS = {
        'HA': int,
    }

    EXTRA_VALIDITY_REQUIREMENTS = {
        'HA': habitat.Habitat.valid_and_liveable,
        'DB': cap_at_100,
        'DR': cap_at_100,
        'BR': cap_at_100,
        'AP': cap_at_100,
    }
    
    NORMAL_STATS = 'level', 'healthMultiplier', 'damageMultiplier', 'speedMultiplier', 'sizeMultiplier', 'sizeScale', \
        'damageBlock', 'damageReflection', 'bleedReduction', 'poisonResistance', 'armorPenetration' 
    BIOME_STATS = 'oxygenTime', 'temperatureTime', 'pressureTime', 'salinityTime' 

    BOOLEANS = ('canFly', 'canSwim', 'canStand', 'breathesInAir', 'breathesInWater', 'canClimb', 'poisonResistant',
                'ungrabbable', 'canDig', 'canWalkUnderwater', 'chooseable', 'hasWalkingAbility')
    
    OLD_STAT_MULTIPLIERS = {
        'DB': 100, 
        'DR': 100, 
        'AP': 100, 
        'BR': 100, 
    }
    STAT_CHANGE_CONVERTERS = {
        'HM': lambda num: tools.trunc_float(num * 100), 
        'DM': lambda num: tools.trunc_float(num * 20), 
        'SS': lambda num: float(num), 
        'HA': lambda num: habitat.Habitat(num), 
    }

    DEEPCORD_ID = 273213133731135500

    SKIN_REVIEW_LIST_URL = 'https://api.deeeep.io/skins/pending?t=review' 
    STATS_UNBALANCE_BLACKLIST = ['OT', 'TT', 'PT', 'ST', 'SS', 'HA'] 
    FLOAT_CHECK_REGEX = '\A(?P<abs_val>[-+][0-9]+(?:\.[0-9]+)?)\Z' 
    REDDIT_LINK_REGEX = '\A(?:https?://)?(?:www\.)?reddit\.com/(?:r|u|(?:user))/[0-9a-zA-Z_]+/comments/[0-9a-zA-Z]+/.+/?(?:\?.*)?\Z' 

    MAP_URL_ADDITION = 's/' 
    MAPMAKER_URL_PREFIX = 'https://mapmaker.deeeep.io/map/'
    MAPMAKER_URL_TEMPLATE = MAPMAKER_URL_PREFIX + '{}'
    MAP_REGEX = '\A(?:(?:https?://)?(?:www\.)?mapmaker\.deeeep\.io/map/)?(?P<map_string_id>[0-9_A-Za-z]+)\Z' 

    PENDING_SKINS_LIST_URL = 'https://apibeta.deeeep.io/skins/pending' 
    PENDING_MOTIONS_URL = 'https://apibeta.deeeep.io/motions/pending?targetType=skin' 
    RECENT_MOTIONS_URL = 'https://apibeta.deeeep.io/motions/recent?targetType=skin' 
    UPCOMING_LIST_URL = 'https://apibeta.deeeep.io/skins/pending?t=upcoming'

    CHARACTER_TEMPLATE = 'https://beta.deeeep.io/assets/characters/{}.png' 

    CHARACTER_EXCEPTIONS = {
        'lanternfish': 'https://deeeep.io/new/assets/characters/lanternfish.png', 
        'pelican': 'https://deeeep.io/new/assets/characters/pelican.png', 
    }

    class AVAILABILITY_FILTERS(enum.Enum):
        hallooween = partial(lambda self, skin: skin['season'] == 'hallooween')
        halloween = partial(lambda self, skin: skin['season'] == 'hallooween')
        christmas = partial(lambda self, skin: skin['season'] == 'christmas')
        valentines = partial(lambda self, skin: skin['season'] == 'valentines')
        easter = partial(lambda self, skin: skin['season'] == 'easter')
        lunar = partial(lambda self, skin: skin['season'] == 'lunar')
        lunar_new_year = partial(lambda self, skin: skin['season'] == 'lunar')
        real = partial(lambda self, skin: skin['category'] == 'real')
        realistic = partial(lambda self, skin: skin['category'] == 'real')
        unrealistic = partial(lambda self, skin: skin['category'] == 'unrealistic')
        season = partial(lambda self, skin: skin['category'] == 'season')
        seasonal = partial(lambda self, skin: skin['category'] == 'season')

    class ACCEPTABILITY_FILTERS(enum.Enum):
        acceptable = partial(lambda self, skin: not self.reject_reasons(skin, check_reddit=False))
        unacceptable = partial(lambda self, skin: self.reject_reasons(skin, check_reddit=False))

    class STAT_CHANGE_FILTERS(enum.Enum):
        stat_changing = partial(lambda self, skin: skin['attributes'])
        non_stat_changing = partial(lambda self, skin: not skin['attributes'])

    class PRICE_FILTERS(enum.Enum):
        free = partial(lambda self, skin: skin['price'] == 0)
        not_free = partial(lambda self, skin: skin['price'] != 0)
    
    class PENDING_FILTERS(enum.Enum):
        reskin = partial(lambda self, skin: skin['parent'] if 'parent' in skin else False)
        not_reskin = partial(lambda self, skin: 'parent' not in skin or not skin['parent'])
    
    print(repr(AVAILABILITY_FILTERS.seasonal))

    # print(PENDING_FILTERS_MAP)

    # SKIN_FILTERS = enum.Enum('SKIN_FILTERS', tuple(PENDING_FILTERS_MAP.keys()), module=__name__)

    # print(list(SKIN_FILTERS))
    
    '''
    PENDING_FILTERS_STR = tools.format_iterable(PENDING_FILTERS.keys(), formatter='`{}`') 
    '''

    SEARCH_LIMIT = 30

    SKIN_STATUS_ATTRS = 'approved', 'upcoming', 'reviewed', 'rejected'

    class IconsEnum(enum.Enum):
        dc = chars.discord, None
        fb = chars.facebook, None
        ig = chars.instagram, 'https://instagram.com/{}'
        qq = chars.qq, None
        rd = chars.reddit, 'https://reddit.com/u/{}'
        tc = chars.twitch, 'https://twitch.tv/{}'
        tw = chars.twitter, 'https://twitter.com/{}'
        vk = chars.vk, None
        wb = chars.weibo, 'https://weibo.com/{}'
        wx = chars.wechat, None
        yt = chars.youtube, None
    
    TIER_EMOJIS = chars.smirk_clownfish, chars.crab_rave, chars.shrug_jellyfish, chars.triggered_squid, chars.shut_seagull, \
        chars.cry_ray, chars.dance_penguin, chars.cooloctopus, chars.chain_breaker_hammerhead, chars.thonk_gsquid
    TIER_COLORS = 0xfdbe62, 0xff5959, 0xfc8ab4, 0xffabab, 0xffffff, 0xfdaffd, 0xf7931e, 0xe47918, 0xdbdbdb, 0x902a2a

    APPROVED_PAGE = 'https://creators.deeeep.io/skins/approved'
    PENDING_PAGE = 'https://creators.deeeep.io/skins/pending'
    STORE_PAGE = 'https://beta.deeeep.io/store/skins'
    UPCOMING_PAGE = 'https://creators.deeeep.io/skinboard/upcoming'

    SKIN_EMBED_LINK_FORMATTER = '[{0[name]}](' + SKIN_STORE_PAGE_PREFIX + '{0[id]})'
    MAP_EMBED_LINK_FORMATTER = '[{0[title]}](' + MAPMAKER_URL_PREFIX + '{0[string_id]})'

    MOTION_CREATION_URL = 'https://apibeta.deeeep.io/motions'