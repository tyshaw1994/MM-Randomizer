from collections import namedtuple
import logging
import random

from Items import ItemFactory

# TODO/FIXME: All these lists should be transfered over to ItemPool.py
# This file should be used as the commented part at the bottom shows.
# The commented part on the bottom also had the record from Items.py,
# which is now deleted and unused.


alwaysitems = [
    "Mirror Shield",
    "Deku Mask",
    "Goron Mask",
    "Zora Mask",
    "Light Arrows",
    "Hookshot"
]

extra_masks = [
    "Postman's Hat",
    "Blast Mask",
    "Great Fairy Mask",
    "All Night Mask",
    "Stone Mask",
    "Keaton Mask",
    "Bremen Mask",
    "Bunny Hood",
    "Don Gero's Mask",
    "Mask of Scents",
    "Romani Mask",
    "Circus Leader Mask",
    "Couple's Mask",
    "Mask of Truth",
    "Kamaro's Mask",
    "Garo Mask",
    "Captain's Hat",
    "Gibdo Mask",
    "Giant Mask"]

notmapcompass = ["Ice Trap"] * 8
rewardlist = ["Odolwa's Remains", "Goht's Remains", "Gyorg's Remains", "Twinmold's Remains"]
songlist = [
    "Song of Time",
    "Song of Healing",
    "Song of Soaring",
    "Epona's Song",
    "Song of Storms",
    "Sonata of Awakening",
    "Goron Lullaby",
    "New Wave Bossa Nova",
    "Elegy of Emptiness",
    "Oath to Order"]

# TODO: this could need to be aligned with the location_table

stray_fairy_locations = (
    ["WF-SF{0}".format(i) for i in range(1,16)] +
    ["SH-SF{0}".format(i) for i in range(1,16)] +
    ["GB-SF{0}".format(i) for i in range(1,16)] +
    ["ST-SF{0}".format(i) for i in range(1,16)])

tradeitems = [
    "Moon's Tear",
    'Town Title Deed',
    'Swamp Title Deed',
    'Mountain Title Deed',
    'Ocean Title Deed'
    ]

extraitems = [
    "Kokiri Sword",
    "Gilded Sword",
    "Great Fairy Sword",
    "Hylian Shield",
    "Fierce Deity Mask",
    "Bow",
    "Large Quiver",
    "Largest Quiver",
    "Fire Arrows",
    "Ice Arrows",
    "Powder Keg",
    "Pictograph Box",
    "Lens of Truth",
    "Bomb Bag",
    "Big Bomb Bag",
    "Biggest Bomb Bag",
    "Adult Wallet",
    "Giant Wallet"
]

WF_vanilla = (['Recovery Heart'] * 2)
SH_vanilla = (['Recovery Heart'] * 2)
GB_vanilla = (['Recovery Heart'] * 2)
ST_vanilla = (['Recovery Heart'] * 2)
PF_vanilla = (['Recovery Heart'] * 2)

normal_bottles = [
    "Bottle",
    "Bottle with Milk",
    "Bottle with Red Potion",
    "Bottle with Green Potion",
    "Bottle with Blue Potion",
    "Bottle with Fairy",
    "Bottle with Fish",
    "Bottle with Bugs",
    "Bottle with Poe",
    "Bottle with Big Poe"]

normal_bottle_count = 6

normal_rupees = (
    ['Rupees (5)'] * 13
    + ['Rupees (20)'] * 5
    + ['Rupees (50)'] * 7
    + ['Rupees (200)'] * 3)

shopsanity_rupees = (
    ['Rupees (5)'] * 2
    + ['Rupees (20)'] * 10
    + ['Rupees (50)'] * 10
    + ['Rupees (200)'] * 5
    + ['Progressive Wallet'])

vanilla_shop_items = {
    'Trading Post Item 1': 'Buy Hylian Shield',
    # TODO: Fill out the rest
}

trade_items = {
    'Moon Tear Crater': "Moon's Tear",
    'Clock Town Deku Salesman': 'Land Title Deed',
    'Swamp Deku Salesman': 'Swamp Title Deed',
    'Mountain Deku Salesman': 'Mountain Title Deed',
    'Ocean Deku Salesman': 'Ocean Title Deed',
    'Canyon Deku Salesman': 'Rupees (200)',
    'Have you seen this man?': 'Letter To Kafei',
    'Item From Kafei': 'Pendant of Memories',
    'Keaton Mask From Kafei': 'Kafei Mask',
    'Letter From Kafei': 'Letter To Mama',
    'We Shall Greet The Morning Together': "Couple's Mask"
}

npc_items = {
    # TODO: List all locations which give items by NPC,
    # and set them to give that specific item
    'Gift From Hungry Goron': "Don Gero's Mask",

}

eventlocations = {
    'Majora': "Majora's Mask"
}


# TODO: I kept this in, because the 'fill_songs' function
# is now in Fill.py, so this should be integrated over there.
def fill_songs(world, attempts=15):
    songs = ItemFactory(songlist)
    song_locations = [
        world.get_location('Song from Skull Kid'),
        world.get_location('Song from HMS'),
        world.get_location('Song from Owl Tablet'),
        world.get_location('Song from Romani'),
        world.get_location('Song at Grave'),
        world.get_location('Song from Monkey'),
        world.get_location('Song from Baby Goron'),
        world.get_location('Song from Goron Elder'),
        world.get_location('Song from Zora Eggs'),
        world.get_location('Song from Igos'),
        world.get_location('Song from the Giants')]
    placed_prizes = [loc.item.name for loc in song_locations if loc.item is not None]
    unplaced_prizes = [song for song in songs if song.name not in placed_prizes]
    empty_song_locations = [loc for loc in song_locations if loc.item is None]

    while attempts:
        attempts -= 1
        try:
            prizepool = list(unplaced_prizes)
            prize_locs = list(empty_song_locations)
            random.shuffle(prizepool)
            random.shuffle(prize_locs)
            # TODO: Set keys to true once keys are properly implemented
            fill_restrictive(world, world.get_all_state(keys=True), prize_locs, prizepool)
        except FillError:
            logging.getLogger('').info("Failed to place songs. Will retry %s more times", attempts)
            for location in empty_song_locations:
                location.item = None
            continue
        break
    else:
        raise FillError('Unable to place songs')

# TODO: This was the format of the OoT fork.
# The MM items should use this format to be able to be processed.
#
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#   THE PREVIOUSLY ADJUSTED RECORD FROM THE OLD MM BRANCH
#  IS FOUND AT THE BOTTOM OF THIS FILE. DO NOT JUST DELETE!
#  (Even though it will probably have to be adjusted first)
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
# # Progressive: True  -> Advancement
# #              False -> Priority
# #              None  -> Normal
# #    Item:                            (type, Progressive, GetItemID, special),
# item_table = {
#     'Bombs (5)':                        ('Item',     None,  0x01, None),
#     'Deku Nuts (5)':                    ('Item',     None,  0x02, None),
#     'Bombchus (10)':                    ('Item',     True,  0x03, None),
#     'Boomerang':                        ('Item',     True,  0x06, None),
#     'Deku Stick (1)':                   ('Item',     None,  0x07, None),
#     'Lens of Truth':                    ('Item',     True,  0x0A, None),
#     'Hammer':                           ('Item',     True,  0x0D, None),
#     'Cojiro':                           ('Item',     True,  0x0E, None),
#     'Bottle':                           ('Item',     True,  0x0F, None),
#     'Bottle with Milk':                 ('Item',     True,  0x14, None),
#     'Bottle with Letter':               ('Item',     True,  0x15, None),
#     'Magic Bean':                       ('Item',     True,  0x16, None),
#     'Skull Mask':                       ('Item',     None,  0x17, None),
#     'Spooky Mask':                      ('Item',     None,  0x18, None),
#     'Keaton Mask':                      ('Item',     None,  0x1A, None),
#     'Bunny Hood':                       ('Item',     None,  0x1B, None),
#     'Mask of Truth':                    ('Item',     None,  0x1C, None),
#     'Pocket Egg':                       ('Item',     True,  0x1D, None),
#     'Pocket Cucco':                     ('Item',     True,  0x1E, None),
#     'Odd Mushroom':                     ('Item',     True,  0x1F, None),
#     'Odd Potion':                       ('Item',     True,  0x20, None),
#     'Poachers Saw':                     ('Item',     True,  0x21, None),
#     'Broken Sword':                     ('Item',     True,  0x22, None),
#     'Prescription':                     ('Item',     True,  0x23, None),
#     'Eyeball Frog':                     ('Item',     True,  0x24, None),
#     'Eyedrops':                         ('Item',     True,  0x25, None),
#     'Claim Check':                      ('Item',     True,  0x26, None),
#     'Kokiri Sword':                     ('Item',     True,  0x27, None),
#     'Deku Shield':                      ('Item',     None,  0x29, None),
#     'Hylian Shield':                    ('Item',     None,  0x2A, None),
#     'Mirror Shield':                    ('Item',     True,  0x2B, None),
#     'Goron Tunic':                      ('Item',     True,  0x2C, None),
#     'Zora Tunic':                       ('Item',     True,  0x2D, None),
#     'Iron Boots':                       ('Item',     True,  0x2E, None),
#     'Hover Boots':                      ('Item',     True,  0x2F, None),
#     'Stone of Agony':                   ('Item',     True,  0x39, None),
#     'Gerudo Membership Card':           ('Item',     True,  0x3A, None),
#     'Heart Container':                  ('Item',     None,  0x3D, None),
#     'Piece of Heart':                   ('Item',     None,  0x3E, None),
#     'Boss Key':                         ('BossKey',  True,  0x3F, None),
#     'Compass':                          ('Compass',  None,  0x40, None),
#     'Map':                              ('Map',      None,  0x41, None),
#     'Small Key':                        ('SmallKey', True,  0x42, {'progressive': True}),
#     'Weird Egg':                        ('Item',     True,  0x47, None),
#     'Recovery Heart':                   ('Item',     None,  0x48, None),
#     'Arrows (5)':                       ('Item',     None,  0x49, None),
#     'Arrows (10)':                      ('Item',     None,  0x4A, None),
#     'Arrows (30)':                      ('Item',     None,  0x4B, None),
#     'Rupee (1)':                        ('Item',     None,  0x4C, None),
#     'Rupees (5)':                       ('Item',     None,  0x4D, None),
#     'Rupees (20)':                      ('Item',     None,  0x4E, None),
#     'Heart Container (Boss)':           ('Item',     None,  0x4F, None),
#     'Goron Mask':                       ('Item',     None,  0x51, None),
#     'Zora Mask':                        ('Item',     None,  0x52, None),
#     'Gerudo Mask':                      ('Item',     None,  0x53, None),
#     'Rupees (50)':                      ('Item',     None,  0x55, None),
#     'Rupees (200)':                     ('Item',     None,  0x56, None),
#     'Biggoron Sword':                   ('Item',     True,  0x57, None),
#     'Fire Arrows':                      ('Item',     True,  0x58, None),
#     'Ice Arrows':                       ('Item',     True,  0x59, None),
#     'Light Arrows':                     ('Item',     True,  0x5A, None),
#     'Gold Skulltula Token':             ('Token',    True,  0x5B, {'progressive': True}),
#     'Dins Fire':                        ('Item',     True,  0x5C, None),
#     'Nayrus Love':                      ('Item',     True,  0x5E, None),
#     'Farores Wind':                     ('Item',     True,  0x5D, None),
#     'Deku Nuts (10)':                   ('Item',     None,  0x64, None),
#     'Bombs (10)':                       ('Item',     None,  0x66, None),
#     'Bombs (20)':                       ('Item',     None,  0x67, None),
#     'Deku Seeds (30)':                  ('Item',     None,  0x69, None),
#     'Bombchus (5)':                     ('Item',     True,  0x6A, None),
#     'Bombchus (20)':                    ('Item',     True,  0x6B, None),
#     'Rupee (Treasure Chest Game)':      ('Item',     None,  0x72, None),
#     'Piece of Heart (Treasure Chest Game)': ('Item', None,  0x76, None),
#     'Ice Trap':                         ('Item',     None, 0x7C,  None),
#     'Progressive Hookshot':             ('Item',     True,  0x80, {'progressive': True}),
#     'Progressive Strength Upgrade':     ('Item',     True,  0x81, {'progressive': True}),
#     'Bomb Bag':                         ('Item',     True,  0x82, None),
#     'Bow':                              ('Item',     True,  0x83, None),
#     'Slingshot':                        ('Item',     True,  0x84, None),
#     'Progressive Wallet':               ('Item',     True,  0x85, {'progressive': True}),
#     'Progressive Scale':                ('Item',     True,  0x86, {'progressive': True}),
#     'Deku Nut Capacity':                ('Item',     None,  0x87, None),
#     'Deku Stick Capacity':              ('Item',     None,  0x88, None),
#     'Bombchus':                         ('Item',     True,  0x89, None),
#     'Magic Meter':                      ('Item',     True,  0x8A, None),
#     'Ocarina':                          ('Item',     True,  0x8B, None),
#     'Bottle with Red Potion':           ('Item',     True,  0x8C, {'shop_object': 0x0F}),
#     'Bottle with Green Potion':         ('Item',     True,  0x8D, {'shop_object': 0x0F}),
#     'Bottle with Blue Potion':          ('Item',     True,  0x8E, {'shop_object': 0x0F}),
#     'Bottle with Fairy':                ('Item',     True,  0x8F, {'shop_object': 0x0F}),
#     'Bottle with Fish':                 ('Item',     True,  0x90, {'shop_object': 0x0F}),
#     'Bottle with Blue Fire':            ('Item',     True,  0x91, {'shop_object': 0x0F}),
#     'Bottle with Bugs':                 ('Item',     True,  0x92, {'shop_object': 0x0F}),
#     'Bottle with Big Poe':              ('Item',     True,  0x93, {'shop_object': 0x0F}),
#     'Bottle with Poe':                  ('Item',     True,  0x94, {'shop_object': 0x0F}),
#     'Boss Key (Forest Temple)':         ('BossKey',  True,  0x95, None),
#     'Boss Key (Fire Temple)':           ('BossKey',  True,  0x96, None),
#     'Boss Key (Water Temple)':          ('BossKey',  True,  0x97, None),
#     'Boss Key (Spirit Temple)':         ('BossKey',  True,  0x98, None),
#     'Boss Key (Shadow Temple)':         ('BossKey',  True,  0x99, None),
#     'Boss Key (Ganons Castle)':         ('BossKey',  True,  0x9A, None),
#     'Compass (Deku Tree)':              ('Compass',  None,  0x9B, None),
#     'Compass (Dodongos Cavern)':        ('Compass',  None,  0x9C, None),
#     'Compass (Jabu Jabus Belly)':       ('Compass',  None,  0x9D, None),
#     'Compass (Forest Temple)':          ('Compass',  None,  0x9E, None),
#     'Compass (Fire Temple)':            ('Compass',  None,  0x9F, None),
#     'Compass (Water Temple)':           ('Compass',  None,  0xA0, None),
#     'Compass (Spirit Temple)':          ('Compass',  None,  0xA1, None),
#     'Compass (Shadow Temple)':          ('Compass',  None,  0xA2, None),
#     'Compass (Bottom of the Well)':     ('Compass',  None,  0xA3, None),
#     'Compass (Ice Cavern)':             ('Compass',  None,  0xA4, None),
#     'Map (Deku Tree)':                  ('Map',      None,  0xA5, None),
#     'Map (Dodongos Cavern)':            ('Map',      None,  0xA6, None),
#     'Map (Jabu Jabus Belly)':           ('Map',      None,  0xA7, None),
#     'Map (Forest Temple)':              ('Map',      None,  0xA8, None),
#     'Map (Fire Temple)':                ('Map',      None,  0xA9, None),
#     'Map (Water Temple)':               ('Map',      None,  0xAA, None),
#     'Map (Spirit Temple)':              ('Map',      None,  0xAB, None),
#     'Map (Shadow Temple)':              ('Map',      None,  0xAC, None),
#     'Map (Bottom of the Well)':         ('Map',      None,  0xAD, None),
#     'Map (Ice Cavern)':                 ('Map',      None,  0xAE, None),
#     'Small Key (Forest Temple)':        ('SmallKey', True,  0xAF, {'progressive': True}),
#     'Small Key (Fire Temple)':          ('SmallKey', True,  0xB0, {'progressive': True}),
#     'Small Key (Water Temple)':         ('SmallKey', True,  0xB1, {'progressive': True}),
#     'Small Key (Spirit Temple)':        ('SmallKey', True,  0xB2, {'progressive': True}),
#     'Small Key (Shadow Temple)':        ('SmallKey', True,  0xB3, {'progressive': True}),
#     'Small Key (Bottom of the Well)':   ('SmallKey', True,  0xB4, {'progressive': True}),
#     'Small Key (Gerudo Training Grounds)':('SmallKey',True, 0xB5, {'progressive': True}),
#     'Small Key (Gerudo Fortress)':('FortressSmallKey',True, 0xB6, {'progressive': True}),
#     'Small Key (Ganons Castle)':        ('SmallKey', True,  0xB7, {'progressive': True}),
#     'Double Defense':                   ('Item',     True,  0xB8, None),
#     'Zeldas Letter':                    ('Item',     True,  None, None),
#     'Master Sword':                     ('Item',     True,  None, None),
#     'Epona':                            ('Event',    True,  None, None),
#     'Deku Stick Drop':                  ('Event',    True,  None, None),
#     'Deku Nut Drop':                    ('Event',    True,  None, None),
#     'Carpenter Rescue':                 ('Event',    True,  None, None),
#     'Forest Trial Clear':               ('Event',    True,  None, None),
#     'Fire Trial Clear':                 ('Event',    True,  None, None),
#     'Water Trial Clear':                ('Event',    True,  None, None),
#     'Shadow Trial Clear':               ('Event',    True,  None, None),
#     'Spirit Trial Clear':               ('Event',    True,  None, None),
#     'Light Trial Clear':                ('Event',    True,  None, None),
#     'Triforce':                         ('Event',    True,  None, None),

#     'Minuet of Forest':                 ('Song',     True,  0xBB,
#                                             {
#                                                 'text_id': 0x73,
#                                                 'song_id': 0x02,
#                                                 'item_id': 0x5A,
#                                             }),
#     'Bolero of Fire':                   ('Song',     True,  0xBC,
#                                             {
#                                                 'text_id': 0x74,
#                                                 'song_id': 0x03,
#                                                 'item_id': 0x5B,
#                                             }),
#     'Serenade of Water':                ('Song',     True,  0xBD,
#                                             {
#                                                 'text_id': 0x75,
#                                                 'song_id': 0x04,
#                                                 'item_id': 0x5C,
#                                             }),
#     'Requiem of Spirit':                ('Song',     True,  0xBE,
#                                             {
#                                                 'text_id': 0x76,
#                                                 'song_id': 0x05,
#                                                 'item_id': 0x5D,
#                                             }),
#     'Nocturne of Shadow':               ('Song',     True,  0xBF,
#                                             {
#                                                 'text_id': 0x77,
#                                                 'song_id': 0x06,
#                                                 'item_id': 0x5E,
#                                             }),
#     'Prelude of Light':                 ('Song',     True,  0xC0,
#                                             {
#                                                 'text_id': 0x78,
#                                                 'song_id': 0x07,
#                                                 'item_id': 0x5F,
#                                             }),
#     'Zeldas Lullaby':                   ('Song',     True,  0xC1,
#                                             {
#                                                 'text_id': 0xD4,
#                                                 'song_id': 0x0A,
#                                                 'item_id': 0x60,
#                                             }),
#     'Eponas Song':                      ('Song',     True,  0xC2,
#                                             {
#                                                 'text_id': 0xD2,
#                                                 'song_id': 0x09,
#                                                 'item_id': 0x61,
#                                             }),
#     'Sarias Song':                      ('Song',     True,  0xC3,
#                                             {
#                                                 'text_id': 0xD1,
#                                                 'song_id': 0x08,
#                                                 'item_id': 0x62,
#                                             }),
#     'Suns Song':                        ('Song',     True,  0xC4,
#                                             {
#                                                 'text_id': 0xD3,
#                                                 'song_id': 0x0B,
#                                                 'item_id': 0x63,
#                                             }),
#     'Song of Time':                     ('Song',     True,  0xC5,
#                                             {
#                                                 'text_id': 0xD5,
#                                                 'song_id': 0x0C,
#                                                 'item_id': 0x64,
#                                             }),
#     'Song of Storms':                   ('Song',     True,  0xC6,
#                                             {
#                                                 'text_id': 0xD6,
#                                                 'song_id': 0x0D,
#                                                 'item_id': 0x65,
#                                             }),

#     'Buy Deku Nut (5)':                 ('Shop',     True,  0x00, {'object': 0x00BB, 'price': 15}),
#     'Buy Arrows (30)':                  ('Shop',     False, 0x01, {'object': 0x00D8, 'price': 60}),
#     'Buy Arrows (50)':                  ('Shop',     False, 0x02, {'object': 0x00D8, 'price': 90}),
#     'Buy Bombs (5) [25]':               ('Shop',     False, 0x03, {'object': 0x00CE, 'price': 25}),
#     'Buy Deku Nut (10)':                ('Shop',     True,  0x04, {'object': 0x00BB, 'price': 30}),
#     'Buy Deku Stick (1)':               ('Shop',     True,  0x05, {'object': 0x00C7, 'price': 10}),
#     'Buy Bombs (10)':                   ('Shop',     False, 0x06, {'object': 0x00CE, 'price': 50}),
#     'Buy Fish':                         ('Shop',     False, 0x07, {'object': 0x00F4, 'price': 200}),
#     'Buy Red Potion [30]':              ('Shop',     False, 0x08, {'object': 0x00EB, 'price': 30}),
#     'Buy Green Potion':                 ('Shop',     False, 0x09, {'object': 0x00EB, 'price': 30}),
#     'Buy Blue Potion':                  ('Shop',     False, 0x0A, {'object': 0x00EB, 'price': 100}),
#     'Buy Hylian Shield':                ('Shop',     False, 0x0C, {'object': 0x00DC, 'price': 80}),
#     'Buy Deku Shield':                  ('Shop',     True,  0x0D, {'object': 0x00CB, 'price': 40}),
#     'Buy Goron Tunic':                  ('Shop',     True,  0x0E, {'object': 0x00F2, 'price': 200}),
#     'Buy Zora Tunic':                   ('Shop',     True,  0x0F, {'object': 0x00F2, 'price': 300}),
#     'Buy Heart':                        ('Shop',     False, 0x10, {'object': 0x00B7, 'price': 10}),
#     'Buy Bombchu (10)':                 ('Shop',     True,  0x15, {'object': 0x00D9, 'price': 99}),
#     'Buy Bombchu (20)':                 ('Shop',     True,  0x16, {'object': 0x00D9, 'price': 180}),
#     'Buy Bombchu (5)':                  ('Shop',     True,  0x18, {'object': 0x00D9, 'price': 60}),
#     'Buy Deku Seeds (30)':              ('Shop',     False, 0x1D, {'object': 0x0119, 'price': 30}),
#     'Sold Out':                         ('Shop',     False, 0x26, {'object': 0x0148}),
#     'Buy Blue Fire':                    ('Shop',     True,  0x27, {'object': 0x0173, 'price': 300}),
#     'Buy Bottle Bug':                   ('Shop',     True,  0x28, {'object': 0x0174, 'price': 50}),
#     'Buy Poe':                          ('Shop',     False, 0x2A, {'object': 0x0176, 'price': 30}),
#     'Buy Fairy\'s Spirit':              ('Shop',     False, 0x2B, {'object': 0x0177, 'price': 50}),
#     'Buy Arrows (10)':                  ('Shop',     False, 0x2C, {'object': 0x00D8, 'price': 20}),
#     'Buy Bombs (20)':                   ('Shop',     False, 0x2D, {'object': 0x00CE, 'price': 80}),
#     'Buy Bombs (30)':                   ('Shop',     False, 0x2E, {'object': 0x00CE, 'price': 120}),
#     'Buy Bombs (5) [35]':               ('Shop',     False, 0x2F, {'object': 0x00CE, 'price': 35}),
#     'Buy Red Potion [40]':              ('Shop',     False, 0x30, {'object': 0x00EB, 'price': 40}),
#     'Buy Red Potion [50]':              ('Shop',     False, 0x31, {'object': 0x00EB, 'price': 50}),

#     'Kokiri Emerald':                   ('Event',    True,  None,
#                                             {
#                                                 'save_byte':  0xA5,
#                                                 'save_bit':   0x04,
#                                                 'addr2_data': 0x80,
#                                                 'bit_mask':   0x00040000,
#                                                 'item_id':    0x6C,
#                                             }),
#     'Goron Ruby':                       ('Event',    True,  None,
#                                             {
#                                                 'save_byte':  0xA5,
#                                                 'save_bit':   0x08,
#                                                 'addr2_data': 0x81,
#                                                 'bit_mask':   0x00080000,
#                                                 'item_id':    0x6D,
#                                             }),
#     'Zora Sapphire':                    ('Event',    True,  None,
#                                             {
#                                                 'save_byte':  0xA5,
#                                                 'save_bit':   0x10,
#                                                 'addr2_data': 0x82,
#                                                 'bit_mask':   0x00100000,
#                                                 'item_id':    0x6E,
#                                             }),
#     'Forest Medallion':                 ('Event',    True,  None,
#                                             {
#                                                 'save_byte':  0xA7,
#                                                 'save_bit':   0x01,
#                                                 'addr2_data': 0x3E,
#                                                 'bit_mask':   0x00000001,
#                                                 'item_id':    0x66,
#                                             }),
#     'Fire Medallion':                   ('Event',    True,  None,
#                                             {
#                                                 'save_byte':  0xA7,
#                                                 'save_bit':   0x02,
#                                                 'addr2_data': 0x3C,
#                                                 'bit_mask':   0x00000002,
#                                                 'item_id':    0x67,
#                                             }),
#     'Water Medallion':                  ('Event',    True,  None,
#                                             {
#                                                 'save_byte':  0xA7,
#                                                 'save_bit':   0x04,
#                                                 'addr2_data': 0x3D,
#                                                 'bit_mask':   0x00000004,
#                                                 'item_id':    0x68,
#                                             }),
#     'Spirit Medallion':                 ('Event',    True,  None,
#                                             {
#                                                 'save_byte':  0xA7,
#                                                 'save_bit':   0x08,
#                                                 'addr2_data': 0x3F,
#                                                 'bit_mask':   0x00000008,
#                                                 'item_id':    0x69,
#                                             }),
#     'Shadow Medallion':                 ('Event',    True,  None,
#                                             {
#                                                 'save_byte':  0xA7,
#                                                 'save_bit':   0x10,
#                                                 'addr2_data': 0x41,
#                                                 'bit_mask':   0x00000010,
#                                                 'item_id':    0x6A,
#                                             }),
#     'Light Medallion':                  ('Event',    True,  None,
#                                             {
#                                                 'save_byte':  0xA7,
#                                                 'save_bit':   0x20,
#                                                 'addr2_data': 0x40,
#                                                 'bit_mask':   0x00000020,
#                                                 'item_id':    0x6B,
#                                             }),
# }

# TODO: These need to be adjusted to the example shown above.
# The hex item codes will also probably have to be double checked.
#
# # Format (old): Name: (Advancement, Priority, Type, ItemCode, Index)
# item_table = {
#     'Bow': (True, False, None, 0x0620, 0x31),
#     'Hookshot': (True, False, None, 0x0120, 0x09),
#     'Bomb Bag': (True, False, None, 0x0680, 0x34),
#     'Big Bomb Bag': (True, False, None, 0x0680, 0x34),
#     'Biggest Bomb Bag': (True, False, None, 0x0680, 0x34),
#     'Lens of Truth': (True, False, None, 0x0140, 0x0A),
#     'Fire Arrows': (True, False, None, 0x0B00, 0x58),
#     'Ice Arrows': (True, False, None, 0x0B20, 0x59),
#     'Light Arrows': (True, False, None, 0x0B40, 0x5A),
#     'Ocarina of Time': (True, False, None, 0x0180, 0x0C),
#     'Bottle': (True, False, None, None, None),
#     'Bottle with Red Potion': (True, False, None, None, None),
#     'Bottle with Gold Dust': (True, False, None, None, None),
#     'Bottle with Milk': (True, False, None, None, None),
#     'Bottle with Chateau Romani': (True, False, None, None, None),
#     'Kokiri Sword': (True, False, None, 0x04E0, 0x27),
#     'Gilded Sword': (True, False, None, 0x04E0, 0x27),
#     'Hylian Shield': (False, False, None, 0x0540, 0x2A),
#     'Mirror Shield': (True, False, None, 0x0560, 0x2B),
#     'Deku Mask': (True, False, None, 0x0580, 0x2C),
#     'Goron Mask': (True, False, None, 0x0580, 0x2C),
#     'Zora Mask': (True, False, None, 0x05A0, 0x2D),
#     'Fierce Deity Mask': (True, False, None, 0x05A0, 0x2D),
#     'Progressive Wallet': (True, False, None, 0x08C0, 0x46),
#     'Piece of Heart': (False, False, None, 0x07C0, 0x3E),
#     'Recovery Heart': (False, True, None, 0x0900, 0x48),
#     'Arrows (5)': (False, True, None, 0x0920, 0x49),
#     'Arrows (10)': (False, True, None, 0x0940, 0x4A),
#     'Arrows (30)': (False, True, None, 0x0960, 0x4B),
#     'Bombs (5)': (False, True, None, 0x0020, 0x01),
#     'Bombs (10)': (False, True, None, 0x0CC0, 0x66),
#     'Bombs (20)': (False, True, None, 0x0CE0, 0x67),
#     'Bombchus (5)': (False, False, None, 0x0D40, 0x6A),
#     'Bombchus (10)': (False, False, None, 0x0060, 0x03),
#     'Bombchus (20)': (False, False, None, 0x0D60, 0x6B),
#     'Deku Nuts (5)': (False, True, None, 0x0040, 0x02),
#     'Deku Nuts (10)': (False, True, None, 0x0C80, 0x64),
#     'Rupee (1)': (False, False, None, 0x0980, 0x4C),
#     'Rupees (5)': (False, False, None, 0x09A0, 0x4D),
#     'Rupees (20)': (False, False, None, 0x09C0, 0x4E),
#     'Rupees (50)': (False, False, None, 0x0AA0, 0x55),
#     'Rupees (100)': (False, False, None, 0x0AC0, 0x56),
#     'Rupees (200)': (False, False, None, 0x0AC0, 0x56),
#     'Ice Trap': (False, True, None, 0x0F80, 0x7C),
#     'Magic Bean': (True, False, None, 0x02C0, 0x16),
#     # 'Map': (False, False, 'Map', 0x0820, 0x41),
#     # 'Compass': (False, False, 'Compass', 0x0800, 0x40),
#     # 'Boss Key': (False, False, 'BossKey', 0x07E0, 0x3F),
#     # 'Small Key': (False, False, 'SmallKey', 0x0840, 0x42),
#     'Map (Woodfall Temple)': (False, False, 'Map', 0x0820, 0x41),
#     'Compass (Woodfall Temple)': (False, False, 'Compass', 0x0800, 0x40),
#     'Boss Key (Woodfall Temple)': (False, False, 'BossKey', 0x07E0, 0x3F),
#     'Small Key (Woodfall Temple)': (False, False, 'SmallKey', 0x0840, 0x42),
#     'Map (Snowhead Temple)': (False, False, 'Map', 0x0820, 0x41),
#     'Compass (Snowhead Temple)': (False, False, 'Compass', 0x0800, 0x40),
#     'Boss Key (Snowhead Temple)': (False, False, 'BossKey', 0x07E0, 0x3F),
#     'Small Key (Snowhead Temple)': (False, False, 'SmallKey', 0x0840, 0x42),
#     'Map (Great Bay Temple)': (False, False, 'Map', 0x0820, 0x41),
#     'Compass (Great Bay Temple)': (False, False, 'Compass', 0x0800, 0x40),
#     'Boss Key (Great Bay Temple)': (False, False, 'BossKey', 0x07E0, 0x3F),
#     'Small Key (Great Bay Temple)': (False, False, 'SmallKey', 0x0840, 0x42),
#     'Map (Stone Tower Temple)': (False, False, 'Map', 0x0820, 0x41),
#     'Compass (Stone Tower Temple)': (False, False, 'Compass', 0x0800, 0x40),
#     'Boss Key (Stone Tower Temple)': (False, False, 'BossKey', 0x07E0, 0x3F),
#     'Small Key (Stone Tower Temple)': (False, False, 'SmallKey', 0x0840, 0x42),
#     'Song of Time': (True, False, 'Song', None, None),
#     'Song of Healing': (True, False, 'Song', None, None),
#     "Epona's Song": (True, False, 'Song', None, None),
#     'Song of Soaring': (True, False, 'Song', None, None),
#     'Song of Storms': (True, False, 'Song', None, None),
#     'Sonata of Awakening': (True, False, 'Song', None, None),
#     'Lullaby Intro': (True, False, 'Song', None, None),
#     'Goron Lullaby': (True, False, 'Song', None, None),
#     'New Wave Bossa Nova': (True, False, 'Song', None, None),
#     'Elegy of Emptiness': (True, False, 'Song', None, None),
#     'Oath to Order': (True, False, 'Song', None, None),
#     'Magic Meter': (True, False, 'Event', None, None),
#     'Epona': (True, False, 'Event', None, None),
#     'CT Stray Fairy Pickup': (True, False, 'Event', None, None),
#     'WF Stray Fairy Pickup': (True, False, 'Event', None, None),
#     'SH Stray Fairy Pickup': (True, False, 'Event', None, None),
#     'GB Stray Fairy Pickup': (True, False, 'Event', None, None),
#     'ST Stray Fairy Pickup': (True, False, 'Event', None, None),
#     "Odolwa's Remains": (True, False, 'Remains', None, None),
#     "Goht's Remains": (True, False, 'Remains', None, None),
#     "Gyorg's Remains": (True, False, 'Remains', None, None),
#     "Twinmold's Remains": (True, False, 'Remains', None, None),
#     "Majoras Mask": (True, False, 'Event', None, None)
#     }

# TODO: This was also found in the now removed Items.py
# But I'm not sure if anything like this is used anywhere?
# Keeping it here just in case it is needed somewhere else in the code.
# (Also pretty sure the hex codes need to be double checked
# if it turns out this is data we need to use.)
#
# item_data = {
#     'Bow': [0x4C, 0x80, 0x17, 0xEE, 0x00, 0xBE],
#     'Progressive Hookshot': [0x0B, 0x80, 0x2E, 0xD7, 0x00, 0xDD],
#     'Bomb Bag': [0x4F, 0x80, 0x1A, 0xD8, 0x00, 0xBF],
#     'Lens of Truth': [0x0F, 0x80, 0x36, 0x39, 0x00, 0xEA],
#     'Fire Arrows': [0x04, 0x80, 0x60, 0x70, 0x01, 0x58],
#     'Ice Arrows': [0x0C, 0x80, 0x61, 0x71, 0x01, 0x58],
#     'Light Arrows': [0x12, 0x80, 0x62, 0x72, 0x01, 0x58],
#     'Bottle': [0x14, 0x80, 0x01, 0x42, 0x00, 0xC6],
#     'Bottle with Red Potion': [0x1B, 0x80, 0x45, 0x99, 0x01, 0x0B],
#     'Bottle with Milk': [0x1A, 0x80, 0x30, 0x98, 0x00, 0xDF],
#     'Kokiri Sword': [0x3B, 0x80, 0x74, 0xA4, 0x01, 0x8D],
#     'Hylian Shield': [0x3F, 0xA0, 0xD4, 0x4D, 0x00, 0xDC],
#     'Mirror Shield': [0x40, 0x80, 0x3A, 0x4E, 0x00, 0xEE],
#     'Deku Mask': [0x42, 0xA0, 0x3C, 0x50, 0x00, 0xF2],
#     'Goron Mask': [0x42, 0xA0, 0x3C, 0x50, 0x00, 0xF2],
#     'Zora Mask': [0x43, 0xA0, 0x3D, 0x51, 0x00, 0xF2],
#     'Fierce Deity Mask': [0x42, 0xA0, 0x3C, 0x50, 0x00, 0xF2],
#     'Progressive Wallet': [0x57, 0x80, 0x23, 0xE9, 0x00, 0xD1],
#     'Piece of Heart': [0x7A, 0x80, 0x14, 0xC2, 0x00, 0xBD],
#     'Recovery Heart': [0x83, 0x80, 0x09, 0x55, 0x00, 0xB7],
#     'Arrows (5)': [0x92, 0x48, 0xDB, 0xE6, 0x00, 0xD8],
#     'Arrows (10)': [0x93, 0x4A, 0xDA, 0xE6, 0x00, 0xD8],
#     'Arrows (30)': [0x94, 0x4A, 0xD9, 0xE6, 0x00, 0xD8],
#     'Bombs (5)': [0x8E, 0x59, 0xE0, 0x32, 0x00, 0xCE],
#     'Bombs (10)': [0x8F, 0x59, 0xE0, 0x32, 0x00, 0xCE],
#     'Bombs (20)': [0x90, 0x59, 0xE0, 0x32, 0x00, 0xCE],
#     'Bombchus (5)': [0x96, 0x80, 0xD8, 0x33, 0x00, 0xD9],
#     'Bombchus (10)': [0x09, 0x80, 0xD8, 0x33, 0x00, 0xD9],
#     'Bombchus (20)': [0x97, 0x80, 0xD8, 0x33, 0x00, 0xD9],
#     'Deku Nuts (1)': [0x8C, 0x0C, 0xEE, 0x34, 0x00, 0xBB],
#     'Deku Nuts (10)': [0x8D, 0x0C, 0xEE, 0x34, 0x00, 0xBB],
#     'Rupee (1)': [0x84, 0x00, 0x93, 0x6F, 0x01, 0x7F],
#     'Rupees (5)': [0x85, 0x01, 0x92, 0xCC, 0x01, 0x7F],
#     'Rupees (20)': [0x86, 0x02, 0x91, 0xF0, 0x01, 0x7F],
#     'Rupees (50)': [0x87, 0x14, 0x8F, 0xF1, 0x01, 0x7F],
#     'Rupees (100)': [0x88, 0x13, 0x8E, 0xF2, 0x01, 0x7F],
#     'Rupees (200)': [0x88, 0x13, 0x8E, 0xF2, 0x01, 0x7F],
#     # Ice Trap in special spots will become a blue rupee.
#     'Ice Trap': [0x85, 0x01, 0x92, 0xCC, 0x01, 0x7F],
#     'Song of Time': 0xD5,
#     'Song of Healing': 0xD3,
#     "Epona's Song": 0xD2,
#     'Song of Soaring': 0xD4,
#     'Song of Storms': 0xD6,
#     'Sonata of Awakening': 0xD7,
#     'Lullaby Intro': 0xD8,
#     'Goron Lullaby': 0xD9,
#     'New Wave Bossa Nova': 0xDA,
#     'Elegy of Emptiness': 0xDB,
#     'Oath to Order': 0xDC,
#     'CT Stray Fairy Pickup': 0xFF,
#     'WF Stray Fairy Pickup': 0xFF,
#     'SH Stray Fairy Pickup': 0xFF,
#     'GB Stray Fairy Pickup': 0xFF,
#     'ST Stray Fairy Pickup': 0xFF,
#     "Odolwa's Remains": 0xDE,
#     "Goht's Remains": 0xDE,
#     "Gyorg's Remains": 0xDE,
#     "Twinmold's Remains": 0xDE
#     }
