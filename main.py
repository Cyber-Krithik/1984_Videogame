import math
import random
import struct
import sys

import pygame

# Configuration and palette
WIDTH = 1100
HEIGHT = 820
FPS = 60

# Dystopian colors
MONO_BG = (16, 20, 18)
CARD_BG = (26, 32, 29)
CARD_BORDER = (50, 65, 57)
TEXT_GREEN = (170, 215, 180)
AMBER_WARNING = (215, 150, 65)
RED_ALERT = (200, 60, 50)
MUTED = (95, 115, 105)
WHITE = (240, 245, 242)
SHADOW = (10, 14, 12)

ENDING_TEXT = {
    "vaporized_coward": (
        "VAPORIZED COWARD. You spent your life avoiding choices. You stayed quiet, looked away when others disappeared, "
        "convinced yourself that invisibility meant safety. Big mistake. The Party noticed your silence and were suspicious. "
        "One evening, the Thought Police knocked on your door. By the morning, your apartment was now occupied by someone else. "
        "Every official record denies you existed. "
    ),
    "vaporized_rebel": (
        "VAPORIZED REBEL. You resisted whenever you could. The diary, the forbidden conversations, the relics of the past. "
        "Eventually, the accumulated evidence piled as impossible evidence for the Party to ignore. "
        "The Thought Police arrived and carried you away. Within days, your records disappeared. "
        "Within weeks, your friends stopped talking about you. History itself now claims you never existed. "
        "As your time came in Room 101, you silently cried. How you wished to carry out the Rebellion, only to be erased. "
    ),
    "room101_betrayed": (
        "ROOM 101 BETRAYED. You believe O'Brien understood you, and you believed rebellion was possible. "
        "You even believed the Brotherhood existed, how naive you were. You were wrong. "
        "The betrayal hurts more than torture. Every conviction, every memory, and every private certainty "
        "is stripped away piece by piece. In the end, there is nothing left to resist with. You love Big Brother. "
    ),
    "room101_loyalist": (
        "ROOM 101 LOYALIST. You tried to serve faithfully. "
        "You followed orders, obeyed directives, repeated every slogan. "
        "But loyalty was never enough. A minor slip became evidence of corruption. "
        "The Party doesn't demand obedience, it demands absolute submission. "
        "Under relentless interrogation, you confess to crimes you never committed. "
        "When the process finally ends, you understand the truth. You love Big Brother. "
    ),
    "insanity": (
        "INSANITY. The strain of doublethink shattered your mind. Memory and reality become impossible to distinguish. "
        "Yesterday changes every day. Truth changes every hour. You wander the streets muttering fragments of Party slogans "
        "and half-forgotten memories. The Party never needed to arrest you. You simply made reality abandon you as a half-baked person. "
    ),
    "converted_loyalist": (
        "CONVERTED LOYALIST. You served faithfully, rewrote history, corrected records, "
        "and repeated every slogan demanded of you. Eventually, the contradictions stopped bothering you. "
        "You believe that two plus two equals five, war is peace, freedom is slavery, and ignorance is strength. "
        "The Party no longer needs to watch you. You have learned to watch yourself. You, for the first time, "
        "feel completely at peace. You love Big Brother. "
    ),
    "empty_bureaucrat": (
        "EMPTY BUREAUCRAT. You neither resisted nor truly believed. "
        "You processed forms, corrected records, and survived by making yourself invisible. "
        "Weeks became months, months became years, no one noticed you, no one remembers you. "
        "When you die alone, your position is filled faster than your body is removed. "
        "The machine continues without interruption, your life changed nothing. Big Brother laughs at you. "
    ),
    "julia_betrayal": (
        "JULIA BETRAYAL. You tried to preserve something human in a world designed to destroy humanity. "
        "You trusted Julia and Julia trusted you. But when the pressure came, both of you broke. "
        "Under the interrogation, the both of you revealed the dark secrets of the other, hoping to be spared. "
        "Months later, you two meet in Victory Square, but neither of you speak nor smile. "
        "Instead, you both walk away in opposite directions with cold, icy eyes and become strangers forever. "
    ),
    "inner_party_informant": (
        "INNER PARTY INFORMANT (VIP ENDING). Your loyalty was flawless. Your record immaculate. "
        "The Party rewarded what it valued most: obedience without hesitation. "
        "You are transported into the security department itself, reviewing surveillance "
        "reports, and identifying thoughtcriminals. "
        "Everyday, you help erase names, rewrite memories, and destroy lives. "
        "You have become the eye you once feared. Years later, while reviewing "
        "classified personal files, you discover a folder bearing your own name. "
        "For the first time in your life, you feel afraid. "
    ),
}

GLOSSARY_TERMS = {
    # Core Political and Social Terms
    "AIRSTRIP ONE": "The name given to the former British colony of England, now part of Oceania under Party control",
    "BIG BROTHER": "The omnipresent leader of the Party, symbolizing constant surveillance and absolute ideological control",
    "DOUBLETHINK": "Holding two contradictory beliefs simultaneously. ",
    "INGSOC": "Newspeak for English Socialism, the official totalitarian ideology of the Party",
    "NEWSPEAK": "The Party's restricted language, designed to make thoughtcrime impossible by eliminating forbidden words",
    "THOUGHTCRIME": "The essential crime; holding unspoken thoughts, doubts, or memories that oppose Party doctrine",
    "THOUGHT POLICE": "The secret police force tasked with monitoring expressions, surveillance, and punishing dissent",

    # Party Institutions and Events
    "MINISTRY OF LOVE": "Miniluv: the Party's prison and torture center for thoughtcriminals, known as the place where there is no darkness",
    "MINISTRY OF PEACE": "Minipax: controls military policy, Oceania's endless war effort, and wartime propaganda",
    "MINISTRY OF PLENTY": "Miniplenty: manages the economic output, rationing, and distribution despite constant shortages",
    "MINISTRY OF TRUTH": "Minitrue: controls all media, news, art, and education. It is the history rewriting machine",
    "HATE WEEK": "A massive, week-long rally organized by Minitrue to get the population to hate on the enemy states",
    "TWO MINUTES HATE": "A daily ritualized rally where party members gather to scream hatred at Emmanuel Goldstein",

    # Cultural and Historical References
    "FLOATING FORTRESS": "A massive, unsinkable floating warship utilized by Oceania's naval forces",
    "JUS PRIMAE NOCTIS": "A fabricated capitalist 'law' cited by Party propaganda claiming capitalist bosses could sleep with any worker",
    "JUNIOR ANTI-SEX LEAGUE": "A young group promoting state-control over human relationships",

    # Other note-worthy terms!
    "BLACK MARKET": "The underground trade circuit where forbidden luxury goods such as real coffee, tea, and sugar are bought",
    "MEMORY HOLE": "Pneumatic tubes leading directly to incinerators where the Party destroys unapproved historical records",
    "ROOM 101": "The ultimate interrogation room located in Miniluv: it is designed to confront the individual's worst fear and force them to love the Party and Big Brother.",
}

# --- EXPANDED 8-STAGE CAMPAIGN WITH DYNAMIC OPTIONS ---
GAME_DAYS = [
    {
        "day": 1,
        "day_title": "MINISTRY OF TRUTH - RECORDS OFFICE (WEEK 1)",
        "day_text": "Directive: Rewrite a 1968 report about agriculture output to show a 40 percent surplus, erasing past shortfalls.",
        "day_options": [
            ("Comply fully with Party demands, erasing all historical discrepancies.", -3, 2, 2, "party"),
            ("Maintain cautious silence and process standard revisions neutrally.", -2, 5, 4, "neutral"),
            ("Subtly inject a microscopic factual error into the figures to defy the Party.", 5, 16, 10, "rebel"),
        ],
        "night_title": "VICTORY MANSIONS - APARTMENT (NIGHT)",
        "night_text": "The telescreen quietly stares at you in the corner. You sit down with a blank-paged journal.",
        "night_options": [
            ("Open the diary and write a forbidden thought about freedom.", 8, 10, 15),
            ("Stare blankly at the journal, put down the pen, and go straight to sleep.", -2, -5, 0),
        ],
    },
    {
        "day": 2,
        "day_title": "MINISTRY OF TRUTH - RECORDS OFFICE (WEEK 2)",
        "day_text": "Directive: Comrade Ogilvy has 'died heroically' in battle. Build his background dossier from scratch.",
        "day_options": [
            ("Fabricate a flawless, fiercely patriotic backstory for the fictional hero.", -3, 2, 3, "party"),
            ("Write a standard, bare-minimum biography without embellishment.", -2, 6, 5, "neutral"),
            ("Embed a hidden satirical word inside Ogilvy's biography mocking Party military claims.", 5, 18, 15, "rebel"),
        ],
        "night_title": "PROLE QUARTER - ALLEYWAY (NIGHT)",
        "night_text": "You take a rare walk through the chaotic, impoverished Prole district away from the telescreens.",
        "night_options": [
            ("Talk briefly with an old prole about what life was like before Big Brother.", 8, 12, 10),
            ("Keep your head down and march straight back home to avoid patrol officers.", -2, -2, 5),
        ],
    },
    {
        "day": 3,
        "day_title": "MINISTRY OF TRUTH - CANTEEN (WEEK 3)",
        "day_text": "Syme boasts with fanatical glee about how the New Dictionary is destroying words to make thoughtcrime literally impossible.",
        "day_options": [
            ("Praise Syme's linguistic zeal and agree that narrowing vocabulary is brilliant.", -4, 1, 2, "party"),
            ("Nod vaguely and change the subject to the canteen's Victory Gin.", -2, 6, 6, "neutral"),
            ("Warn Syme quietly that his extreme intelligence makes him a dangerous target.", 4, 15, 15, "rebel"),
        ],
        "night_title": "VICTORY MANSIONS - APARTMENT (NIGHT)",
        "night_text": "A neighbor, Mr. Parsons, bangs on your door asking for razor blades and praising the Junior Spies.",
        "night_options": [
            ("Nod politely, praise the Spies, and hand over the blades to look normal.", -4, -4, 5),
            ("Dismiss him sharply and shut the door in his face.", -2, 14, 10),
        ],
    },
    {
        "day": 4,
        "day_title": "ANTIQUE SHOP - PROLE QUARTER (WEEK 4)",
        "day_text": "In Mr. Charrington's dusty shop, you discover a heavy glass paperweight containing a pink coral core.",
        "day_options": [
            ("Purchase the paperweight as a tangible bridge to a forgotten, beautiful past.", 10, 14, 22, "rebel"),
            ("Realize the extreme danger of possessing antiques and leave it behind.", -2, 4, 4, "neutral"),
            ("Report the antique shop owner to internal security to prove your loyalty.", -4, 0, 0, "party"),
        ],
        "night_title": "VICTORY MANSIONS - APARTMENT (NIGHT)",
        "night_text": "You return to your apartment and consider how to protect yourself from the Party. ",
        "night_options": [
            ("Reflect on a memory that helps you resist Party doublethink.", 10, 8, 15),
            ("Keep a low profile and avoid drawing attention to your apartment", 2, 2, 5),
        ],
    },
    {
        "day": 5,
        "day_title": "MINISTRY OF TRUTH - RECORDS OFFICE (WEEK 5)",
        "day_text": "Directive: Erase all photographic evidence and records of three disgraced Party members who confessed to treason.",
        "day_options": [
            ("Airbrush the photograph cleanly so the traitors never existed.", -3, 3, 3, "party"),
            ("Delay the filing work under a mountain of bureaucratic paperwork.", -2, 8, 8, "neutral"),
            ("Slip the original unedited photograph inside a heavy dictionary on your shelf.", 8, 20, 15, "rebel"),
        ],
        "night_title": "THE GOLDEN COUNTRY - SECRET MEETING (NIGHT)",
        "night_text": "You meet the dark-haired girl, Julia, in a secluded country clearing beyond surveillance.",
        "night_options": [
            ("Open your heart to Julia, planning deeper anti-Party subversion together.", 12, 18, 25),
            ("Remain cautious and guarded, keeping your distance to protect yourself.", 2, 4, 10),
        ],
    },
    {
        "day": 6,
        "day_title": "MINISTRY OF TRUTH - CORRIDOR (WEEK 6)",
        "day_text": "O'Brien passes you in the hall, making subtle eye contact and offering to lend you his copy of the new dictionary.",
        "day_options": [
            ("Politely decline and walk away quickly to avoid senior staff scrutiny.", -3, 2, 5, "party"),
            ("Accept the book cautiously while maintaining strict neutral speech.", 2, 10, 15, "neutral"),
            ("Express subtle, veiled agreement with his dissenting reputation.", 8, 22, 35, "rebel"),
        ],
        "night_title": "VICTORY MANSIONS - RENTED ROOM (NIGHT)",
        "night_text": "You and Julia spend an evening in the secret room above Mr. Charrington's shop, pretending you are free.",
        "night_options": [
            ("Pledge yourselves fully to the underground resistance and the Brotherhood.", 12, 20, 35),
            ("Focus only on each other, ignoring the inevitable doom hanging over you.", 5, 8, 15),
        ],
    },
    {
        "day": 7,
        "day_title": "MINISTRY OF TRUTH - HATE WEEK RALLY (WEEK 7)",
        "day_text": "Hate Week reaches its climax. The enemy superstate suddenly shifts from Eurasia to Eastasia mid-rally.",
        "day_options": [
            ("Instantly scream condemnation at Eastasia, tearing down old banners with fanatic speed.", -4, 1, 4, "party"),
            ("Look around in bewildered silence until others start shouting.", -3, 8, 10, "neutral"),
            ("Fumble your banner change, looking exhausted and visibly cynical.", 6, 24, 30, "rebel"),
        ],
        "night_title": "VICTORY MANSIONS - APARTMENT (NIGHT)",
        "night_text": "A sudden, sharp knock echoes at your apartment door late at night. The air grows cold.",
        "night_options": [
            ("Open the door calmly, ready to face whatever consequence awaits.", -8, 30, 15),
            ("Quickly try to burn your diary pages in the kitchen sink before answering.", 4, 20, 20),
        ],
    },
    {
        "day": 8,
        "day_title": "MINISTRY OF TRUTH - FINAL DIRECTIVE (WEEK 8)",
        "day_text": "Final Ministry Task: Certify the complete elimination of historical records pertaining to Goldstein's inner circle.",
        "day_options": [
            ("Stamp final approval on the state purge documents with total bureaucratic compliance.", -4, 2, 5, "party"),
            ("Submit the clearance forms quietly without reading the dossier.", -2, 10, 10, "neutral"),
            ("Refuse to sign the final clearance sheet, leaving a glaring paper trail.", 10, 35, 45, "rebel"),
        ],
        "night_title": "INNER SANCTUM - O'BRIEN'S STUDY (NIGHT)",
        "night_text": "You arrive at O'Brien's luxurious apartment for your final briefing into the underground Brotherhood.",
        "night_options": [
            ("Pledge absolute allegiance to commit sabotage, terror, and treason.", 8, 25, 40),
            ("Express deep doubts about whether victory against the Party is even possible.", 2, 12, 20),
        ],
    },
]


def synth_hum(frequency=110, duration=1.0, volume=0.012):
    sample_rate = 22050
    sample_count = int(sample_rate * duration)
    buffer = bytearray()
    for index in range(sample_count):
        time = index / sample_rate
        sample = math.sin(2 * math.pi * frequency * time) * volume
        buffer.extend(struct.pack("<h", int(sample * 32767)))
    return pygame.mixer.Sound(buffer=bytes(buffer))


class AudioSystem:
    def __init__(self):
        self.enabled = False
        self.hum = None

        try:
            pygame.mixer.init(frequency = 22050, size =-16, channels=1)
            self.hum = synth_hum(80, 4.0, 0.01)
            self.enabled = True
        except Exception:
            self.enabled = False
            self.hum = None

    def start_hum(self):
        if self.enabled and not pygame.mixer.get_busy():
            self.hum.play(loops=-1)

    def stop(self):
        if self.enabled:
            pygame.mixer.stop()


class OrwellGameAdvanced:
    def __init__(self):
        self.state = "playing"
        self.day_index = 0
        self.phase = "day"

        self.sanity = 75
        self.suspicion = 0
        self.suspicion_limit = random.randint(65, 85)  # Scaled for 8-stage campaign
        self.brotherhood = 10

        # Secondary Hidden Consequences / Flags
        self.has_paperweight = False
        self.identity = 0
        self.julia_trust = 0

        self.party_choices = 0
        self.rebel_choices = 0

        self.log = ["SYSTEM INITIALIZED: Welcome to the Ministry of Truth!"]
        self.current_selection = None
        self.notice = "Week 1: Process the Ministry documents carefully."
        self.ending = None

    @property
    def current_data(self):
        if self.day_index < len(GAME_DAYS):
            return GAME_DAYS[self.day_index]
        return None

    def finish(self, ending_type):
        self.ending = ending_type
        self.state = "ending"

    def trigger_paranoia_event(self):
        """Random stochastic interrogation / telescreen check events."""
        chance = min(0.5, 0.1 + (self.suspicion / 200))
        if random.random() < chance:
            spike = random.randint(
                3 + self.suspicion // 25,
                8 + self.suspicion // 20
            )
            self.suspicion += spike

            events = [
                "A harsh voice from the Telescreen suddenly barks your name, ordering you to correct your posture.",
                "You notice a Junior Spy staring suspiciously at your micro-expressions in the hallway.",
                "A sudden midnight neighborhood patrol guard bangs on your apartment door, inspecting resident papers.",
            ]

            chosen_event = random.choice(events)
            self.log.append(f"PARANOIA ALERT: {chosen_event}")

    def choose_day_action(self, option_index):
        if self.state != "playing" or self.phase != "day":
            return

        data = self.current_data
        opt = data["day_options"][option_index]

        # Apply option impacts (sanity_delta, suspicion_delta, brotherhood_delta)
        self.sanity = max(0, min(100, self.sanity + opt[1]))
        self.suspicion = max(0, self.suspicion + opt[2])
        self.brotherhood = min(100, self.brotherhood + opt[3])
        self.log.append(f"Week {data['day']} (Day): {opt[0]}")

        label = opt[4]
        if label == "party":
            self.party_choices+=1
            self.identity -= 1
            self.suspicion= max(0, self.suspicion - 4)
            if self.party_choices == 3:
                self.log.append("MINISTRY COMMENDATION: Your unwavering orthodoxy earned you inner party praise. ")
            elif self.party_choices >= 5:
                self.log.append("PROMOTION: You have been promoted for exemplary loyalty to the Party. ")
        elif label == "rebel":
            self.rebel_choices += 1
            self.identity += 1
            self.julia_trust += 5
        elif label == "neutral":
            self.identity += 0

        # Check for secondary inventory flags
        if data["day"] == 4 and option_index == 0:
            self.has_paperweight = True
            self.log.append("INVENTORY: You acquired the glass paperweight.")

        self._check_metrics()

        if self.state == "playing":
            self.trigger_paranoia_event()
            self._check_metrics()

        if self.state == "playing":
            self.phase = "night"
            self.notice = "Night Phase: Manage your apartment and journal activities"

    def choose_night_action(self, index):
        if self.state != "playing" or self.phase != "night":
            return

        data=self.current_data
        opt = data["night_options"][index]

        trust_bonus = 3 if self.julia_trust > 15 and index == 0 else 0
        sanity_bonus = 5 if self.has_paperweight and index == 0 else 0

        if index == 0:
            self.identity += 1
        else: 
            self.identity -= 1

        self.sanity = max(0, min(100, self.sanity + opt[1] + trust_bonus + sanity_bonus))
        self.suspicion += opt[2]
        self.brotherhood = min(100, self.brotherhood + opt[3])

        self.log.append(f"Week {data['day']} (Night): {opt[0]}")

        self._check_metrics()
        if self.state == "playing":
            self.day_index += 1
            if self.day_index >= len(GAME_DAYS):
                self.phase = "climax"
                self.notice = "CLIMAX: You meet O'Brien at the Inner Party Ministry."
            else:
                self.phase = "day"
                self.notice = f"Week {self.current_data['day']}: Proceeding to Ministry Records."

    def choose_climax_action(self, option_index):
        if self.state != "playing" or self.phase != "climax":
            return

        if option_index == 0:
            if self.identity <= -3 and self.party_choices >= 5:
                self.log.append("CLIMAX: A black car arrives outside the ministry. Your transfer is approved. ")
                self.finish("inner_party_informant")
            elif self.identity <= -2:
                self.log.append("CLIMAX: You served the Party faithfully, rewriting history until your own past vanished. ")
                self.finish("converted_loyalist")
            else:
                self.log.append("CLIMAX: You tried to serve the Party, but your own secrets betrayed you. ")
                self.finish("room101_loyalist")

        elif option_index == 1:
            if 3 <= self.identity <= 5:
                self.log.append("CLIMAX: Isolated and gripped by paranoia, you and Julia broke under pressure. ")
                self.finish("julia_betrayal")
            else:
                self.log.append("CLIMAX: You drifted through the Ministry as a silent, gray ghost, avoiding every spark of life. ")
                self.finish("empty_bureaucrat")
        elif option_index == 2:
            if self.identity >= 3:
                self.log.append("CLIMAX: O'Brien listens to your deep-seated treason with cold, clinical respect. Room 101 awaits for you. ")
                self.finish("room101_betrayed")
            else:
                self.log.append("CLIMAX: You attempted defiance, but your shallow commitment collapsed instantly under investigation. ")
                self.finish("room101_betrayed")

    def trigger_climax(self):
        if self.state != "playing" or self.phase != "climax":
            return

        if self.identity <= -6 and self.suspicion <= 10 and self.party_choices >= 6 and self.rebel_choices <= 1 and not self.has_paperweight and self.julia_trust <= 5:
            self.log.append("INNER PARTY INFORMANT. Your loyalty was flawless. Your record immaculate. ")
            self.log.append("The Party rewarded what it valued most: obedience without hesitation. ")
            self.log.append("You are transported into the security department itself, reviewing surveillance ")
            self.log.append("reports, and identifying thoughtcriminals. ")
            self.log.append("Everyday, you help erase names, rewrite memories, and destroy lives. ")
            self.log.append("You have become the eye you once feared. Years later, while reviewing ")
            self.log.append("classified personal files, you discover a folder bearing your own name. ")
            self.log.append("For the first time in your life, you feel afraid. ")
            self.finish("inner_party_informant")
        elif -7 <= self.identity <= -3:
            if self.suspicion > 30:
                self.log.append("ROOM 101 LOYALIST. You tried to serve faithfully. ")
                self.log.append("You followed orders, obeyed directives, repeated every slogan. ")
                self.log.append("But loyalty was never enough. A minor slip became evidence of corruption. ")
                self.log.append("The Party doesn't demand obedience, it demands absolute submission. ")
                self.log.append("Under relentless interrogation, you confess to crimes you never committed. ")
                self.log.append("When the process finally ends, you understand the truth. You love Big Brother. ")
                self.finish("room101_loyalist")
            else:
                self.log.append("CONVERTED LOYALIST. You served faithfully, rewrote history, corrected records, ")
                self.log.append("and repeated every slogan demanded of you. Eventually, the contradictions stopped bothering you. ")
                self.log.append("You believe that two plus two equals five, war is peace, freedom is slavery, and ignorance is strength. ")
                self.log.append("The Party no longer needs to watch you. You have learned to watch yourself. You, for the first time, ")
                self.log.append("feel completely at peace. You love Big Brother. ")
                self.finish("converted_loyalist")
        elif -1 <= self.identity <= 1:
            self.log.append("EMPTY BUREAUCRAT. You neither resisted nor truly believed. ")
            self.log.append("You processed forms, corrected records, and survived by making yourself invisible. ")
            self.log.append("Weeks became months, months became years, no one noticed you, no one remembers you. ")
            self.log.append("When you die alone, your position is filled faster than your body is removed. ")
            self.log.append("The machine continues without interruption, your life changed nothing. Big Brother laughs at you. ")
            self.finish("empty_bureaucrat")
        elif 3 <= self.identity <= 5:
            self.log.append("JULIA BETRAYAL. You tried to preserve something human in a world designed to destroy humanity. ")
            self.log.append("You trusted Julia and Julia trusted you. But when the pressure came, both of you broke. ")
            self.log.append("Under the interrogation, the both of you revealed the dark secrets of the other, hoping to be spared. ")
            self.log.append("Months later, you two meet in Victory Square, but neither of you speak nor smile. ")
            self.log.append("Instead, you both walk away in opposite directions with cold, icy eyes and become strangers forever. ")
            self.finish("julia_betrayal")
        elif self.identity >= 6 and self.brotherhood >= 80:
            self.log.append("ROOM 101 BETRAYED. You believe O'Brien understood you, and you believed rebellion was possible. ")
            self.log.append("You even believed the Brotherhood existed, how naive you were. You were wrong. ")
            self.log.append("The betrayal hurts more than torture. Every conviction, every memory, and every private certainty ")
            self.log.append("is stripped away piece by piece. In the end, there is nothing left to resist with. You love Big Brother. ")
            self.finish("room101_betrayed")
        else:
            self.log.append("ROOM 101 BETRAYED. You believe O'Brien understood you, and you believed rebellion was possible. ")
            self.log.append("You even believed the Brotherhood existed, how naive you were. You were wrong. ")
            self.log.append("The betrayal hurts more than torture. Every conviction, every memory, and every private certainty ")
            self.log.append("is stripped away piece by piece. In the end, there is nothing left to resist with. You love Big Brother. ")
            self.finish("room101_betrayed")

    def _check_metrics(self):
        if self.suspicion >= self.suspicion_limit:
            if self.brotherhood>30:
                self.finish("vaporized_rebel")
            else:
                self.finish("vaporized_coward")
        elif self.sanity <= 0:
            self.finish("insanity")


def wrap_text(font, text, width):
    lines = []
    line = ""
    for word in text.split():
        candidate = f"{line} {word}".strip()
        if line and font.size(candidate)[0] > width:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines


def draw_paragraph(surface, text, font, color, rect, line_gap=4, max_lines=None):
    lines = wrap_text(font, text, rect.width)
    if max_lines is not None:
        lines = lines[:max_lines]
    y = rect.y
    for line in lines:
        img = font.render(line, True, color)
        surface.blit(img, (rect.x, y))
        y += img.get_height() + line_gap
    return y


def draw_dashboard(surface, game, fonts, mouse_pos):
    title_font, body_font, small_font = fonts
    surface.fill(MONO_BG)

    header = pygame.Rect(0, 0, WIDTH, 60)
    pygame.draw.rect(surface, (12, 16, 14), header)
    surface.blit(title_font.render("MINISTRY OF TRUTH // SECURE TERMINAL", True, TEXT_GREEN), (24, 16))
    glossary_btn = pygame.Rect(WIDTH-290, 14, 120, 32)
    g_hover = glossary_btn.collidepoint(mouse_pos)
    pygame.draw.rect(surface, (40, 52, 46) if g_hover else CARD_BG, glossary_btn, border_radius = 6)
    pygame.draw.rect(surface, TEXT_GREEN if g_hover else CARD_BORDER, glossary_btn, 1, border_radius = 6)
    g_text = small_font.render("[GLOSSARY]", True, WHITE)
    surface.blit(g_text, g_text.get_rect(center=glossary_btn.center))
    surface.blit(small_font.render("ESC: Quit", True, MUTED), (WIDTH-150, 22))

    metrics_rect = pygame.Rect(26, 74, 1048, 90)
    pygame.draw.rect(surface, CARD_BG, metrics_rect, border_radius=10)
    pygame.draw.rect(surface, CARD_BORDER, metrics_rect, 2, border_radius=10)

    surface.blit(small_font.render("PSYCHOLOGICAL SANITY", True, WHITE), (46, 88))
    s_bar = pygame.Rect(46, 110, 460, 16)
    pygame.draw.rect(surface, (18, 24, 21), s_bar, border_radius=4)
    s_fill = int(460 * (game.sanity / 100))
    s_col = TEXT_GREEN if game.sanity > 40 else (AMBER_WARNING if game.sanity > 20 else RED_ALERT)
    if s_fill > 0:
        pygame.draw.rect(surface, s_col, (46, 110, s_fill, 16), border_radius=4)
    pygame.draw.rect(surface, CARD_BORDER, s_bar, 1, border_radius=4)

    surface.blit(small_font.render("BROTHERHOOD INFILTRATION PROGRESS", True, WHITE), (540, 88))
    b_bar = pygame.Rect(540, 110, 460, 16)
    pygame.draw.rect(surface, (18, 24, 21), b_bar, border_radius=4)
    b_fill = int(460 * (min(100, game.brotherhood) / 100))
    if b_fill > 0:
        pygame.draw.rect(surface, TEXT_GREEN, (540, 110, b_fill, 16), border_radius=4)
    pygame.draw.rect(surface, CARD_BORDER, b_bar, 1, border_radius=4)

    story_rect = pygame.Rect(26, 178, 680, 520)
    pygame.draw.rect(surface, CARD_BG, story_rect, border_radius=12)
    pygame.draw.rect(surface, CARD_BORDER, story_rect, 2, border_radius=12)

    log_rect = pygame.Rect(726, 178, 348, 520)
    pygame.draw.rect(surface, CARD_BG, log_rect, border_radius=12)
    pygame.draw.rect(surface, CARD_BORDER, log_rect, 2, border_radius=12)

    if game.state == "playing":
        data = game.current_data
        if game.phase == "day":
            surface.blit(title_font.render(data["day_title"], True, WHITE), (48, 198))
            draw_paragraph(surface, data["day_text"], body_font, TEXT_GREEN, pygame.Rect(48, 240, 630, 80))

            # Dynamic Day Options Loop
            for idx, opt in enumerate(data["day_options"]):
                d_rect = pygame.Rect(48, 335 + idx * 105, 630, 95)
                d_hover = d_rect.collidepoint(mouse_pos)
                pygame.draw.rect(surface, (40, 52, 46) if d_hover else CARD_BG, d_rect, border_radius=8)
                pygame.draw.rect(surface, TEXT_GREEN if d_hover else CARD_BORDER, d_rect, 2, border_radius=8)
                draw_paragraph(surface, f"• {opt[0]}", small_font, WHITE, pygame.Rect(60, 345 + idx * 105, 606, 75))

        elif game.phase == "night":
            surface.blit(title_font.render(data["night_title"], True, WHITE), (48, 198))
            draw_paragraph(surface, data["night_text"], body_font, TEXT_GREEN, pygame.Rect(48, 240, 630, 100))

            for idx, opt in enumerate(data["night_options"]):
                n_rect = pygame.Rect(48, 380 + idx * 100, 630, 80)
                n_hover = n_rect.collidepoint(mouse_pos)
                pygame.draw.rect(surface, (40, 52, 46) if n_hover else CARD_BG, n_rect, border_radius=8)
                pygame.draw.rect(surface, TEXT_GREEN if n_hover else CARD_BORDER, n_rect, 2, border_radius=8)
                draw_paragraph(surface, f"• {opt[0]}", small_font, WHITE, pygame.Rect(60, 392 + idx * 100, 606, 60))

        elif game.phase == "climax":
            surface.blit(title_font.render("THE INNER PARTY - MEET O'BRIEN", True, WHITE), (48, 198))
            climax_text = (
                "You stand alone in O'Brien's luxurious study. The telescreen sits quietly in the corner. "
                "O'Brien looks at you with a penetrating gaze, waiting for your declaration. "
                "How would you like to respond to him? "
            )
            draw_paragraph(surface, climax_text, body_font, TEXT_GREEN, pygame.Rect(48, 240, 630, 90))
            climax_options = [
                "1. Affirm absolute loyalty to the party and request an inner-party assignment. ",
                "2. Maintain cautious silence, offering standard bureaucratic compliance. ",
                "3. Speak your innermost rebellious thoughts and pledge absolute allegiance with the Brotherhood. "
            ]

            for idx, opt_text in enumerate(climax_options):
                c_rect = pygame.Rect(48, 355 + idx * 105, 630, 95)
                c_hover = c_rect.collidepoint(mouse_pos)
                pygame.draw.rect(surface, (40, 52, 46) if c_hover else CARD_BG, c_rect, border_radius=8)
                pygame.draw.rect(surface, TEXT_GREEN if c_hover else CARD_BORDER, c_rect, 2, border_radius = 8)
                draw_paragraph(surface, f"• {opt_text}", small_font, WHITE, pygame.Rect(60, 365 + idx * 105, 606, 75))

    surface.blit(body_font.render("CHRONICLE LOG", True, TEXT_GREEN), (746, 198))
    log_y = 238
    for entry in game.log[-11:]:
        for line in wrap_text(small_font, entry, 310)[:2]:
            img = small_font.render(line, True, MUTED if not "Week" in line else WHITE)
            surface.blit(img, (746, log_y))
            log_y += 20
        log_y += 4
        if log_y > 670:
            break

    notice_rect = pygame.Rect(26, 712, 1048, 48)
    pygame.draw.rect(surface, CARD_BG, notice_rect, border_radius=8)
    pygame.draw.rect(surface, CARD_BORDER, notice_rect, 1, border_radius=8)
    draw_paragraph(
        surface,
        game.notice,
        small_font,
        WHITE,
        pygame.Rect(
            notice_rect.x+12,
            notice_rect.y+4,
            notice_rect.width-24,
            notice_rect.height-8,
        ),
        line_gap = 2,
        max_lines = 2,
    )

    pygame.display.flip()


def draw_ending(surface, game, fonts):
    title_font, body_font, small_font = fonts
    surface.fill(SHADOW)

    ENDING_HEADINGS = {
        "vaporized_coward": "VAPORIZED BY THE STATE",
        "vaporized_rebel": "VAPORIZED BY THE STATE",
        "room101_betrayed": "SESSION TERMINATED - ROOM 101",
        "room101_loyalist": "SESSION TERMINATED - ROOM 101",
        "insanity": "PSYCHOLOGICAL COLLAPSE",
        "converted_loyalist": "BIG BROTHER LOVES YOU",
        "empty_bureaucrat": "THE FORGOTTEN CITIZEN",
        "julia_betrayal": "LOVE ISN'T LOYALTY",
        "inner_party_informant": "INNER PARTY PROMOTION",
    }

    heading = ENDING_HEADINGS.get(game.ending, "SESSION TERMINATED")
    
    img = title_font.render(heading, True, RED_ALERT)
    surface.blit(img, img.get_rect(center = (WIDTH // 2, 260)))

    prompt = small_font.render("PRESS 'R' TO RESTART SESSION | ESC TO EXIT", True, MUTED)
    surface.blit(prompt, prompt.get_rect(center=(WIDTH // 2, 640)))

    draw_paragraph(
        surface,
        ENDING_TEXT[game.ending],
        body_font,
        WHITE,
        pygame.Rect(180, 340, 740, 200),
        line_gap=10,
    )

    pygame.display.flip()

def draw_glossary(surface, fonts, mouse_pos):
    title_font, _, small_font = fonts
    surface.fill(MONO_BG)

    header = pygame.Rect(0,0, WIDTH, 60)
    pygame.draw.rect(surface, (12, 16, 14), header)
    surface.blit(title_font.render("MINISTRY LEXICON - 1984 Glossary", True, TEXT_GREEN), (24,16))

    back_btn = pygame.Rect(WIDTH - 160, 14, 140, 32)
    b_hover = back_btn.collidepoint(mouse_pos)
    pygame.draw.rect(surface, (40, 52, 46) if b_hover else CARD_BG, back_btn, border_radius =6)
    pygame.draw.rect(surface, TEXT_GREEN if b_hover else CARD_BORDER, back_btn, 1, border_radius=6)
    b_img = small_font.render("[ESC / BACK]", True, WHITE)
    surface.blit(b_img, b_img.get_rect(center=back_btn.center))

    # Scrollable / Container Panel
    content_rect = pygame.Rect(26, 80, 1048, 710)
    pygame.draw.rect(surface, CARD_BG, content_rect, border_radius=12)
    pygame.draw.rect(surface, CARD_BORDER, content_rect, 2, border_radius=12)

    y_offset = 95
    for term, definition in GLOSSARY_TERMS.items():
        if y_offset > 760:  # Stay inside UI bounds
            break
        term_surf = small_font.render(f"• {term}:", True, AMBER_WARNING)
        surface.blit(term_surf, (45, y_offset))
        
        def_lines = wrap_text(small_font, definition, 980)
        y_offset += 18
        for line in def_lines:
            line_surf = small_font.render(line, True, WHITE)
            surface.blit(line_surf, (65, y_offset))
            y_offset += 17
        y_offset += 6

    pygame.display.flip()


def main():
    pygame.init()
    pygame.display.set_caption("1984: Ministry of Truth Advanced Simulation")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    fonts = (
        pygame.font.SysFont("Courier New", 20, bold=True),
        pygame.font.SysFont("Courier New", 16, bold=True),
        pygame.font.SysFont("Courier New", 14),
    )

    game = OrwellGameAdvanced()
    audio = AudioSystem()
    running = True

    while running:
        if game.state == "playing":
            audio.start_hum()
        else:
            audio.stop()

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game.state == "glossary":
                        game.state = "playing"
                    else:
                        running = False
                elif game.state == "ending" and event.key == pygame.K_r:
                    game = OrwellGameAdvanced()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    glossary_btn = pygame.Rect(WIDTH - 290, 14, 120, 32)
                    back_btn = pygame.Rect(WIDTH - 160, 14, 140, 32)

                    # Toggle into and out of Glossary
                    if game.state == "playing" and glossary_btn.collidepoint(mouse_pos):
                        game.state = "glossary"
                    elif game.state == "glossary" and back_btn.collidepoint(mouse_pos):
                        game.state = "playing"

                    # Day / Night / Climax Actions
                    elif game.state == "playing":
                        data = game.current_data
                        if game.phase == "day":
                            for idx in range(len(data["day_options"])):
                                d_rect = pygame.Rect(48, 335 + idx * 105, 630, 95)
                                if d_rect.collidepoint(mouse_pos):
                                    game.choose_day_action(idx)
                        elif game.phase == "night":
                            for idx in range(len(data["night_options"])):
                                n_rect = pygame.Rect(48, 380 + idx * 100, 630, 80)
                                if n_rect.collidepoint(mouse_pos):
                                    game.choose_night_action(idx)
                        elif game.phase == "climax":
                            for idx in range(3):
                                c_rect = pygame.Rect(48, 355 + idx * 105, 630, 95)
                                if c_rect.collidepoint(mouse_pos):
                                    game.choose_climax_action(idx)

        # Draw exactly one screen for the current state.
        if game.state == "playing":
            draw_dashboard(screen, game, fonts, mouse_pos)
        elif game.state == "glossary":
            draw_glossary(screen, fonts, mouse_pos)
        else:
            draw_ending(screen, game, fonts)

        clock.tick(FPS)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()