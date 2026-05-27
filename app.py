import streamlit as st
import json
from pathlib import Path

st.set_page_config(
    page_title="Shinobi Log · Naruto Watch Tracker",
    page_icon="🍥",
    layout="wide",
    initial_sidebar_state="expanded",
)

PROGRESS_FILE = Path(__file__).parent / "progress.json"

# ─────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
    .stExpander > details > summary {font-weight: 600;}
    div[data-testid="stMetricValue"] {font-size: 2rem; font-weight: 800;}
    .badge-canon  {display:inline-block;padding:2px 9px;border-radius:999px;font-size:11px;font-weight:700;background:rgba(72,144,208,0.15);color:#2870b0;border:1px solid rgba(72,144,208,0.4);}
    .badge-filler {display:inline-block;padding:2px 9px;border-radius:999px;font-size:11px;font-weight:700;background:rgba(120,80,192,0.15);color:#5830a0;border:1px solid rgba(120,80,192,0.4);}
    .badge-mixed  {display:inline-block;padding:2px 9px;border-radius:999px;font-size:11px;font-weight:700;background:rgba(200,136,16,0.15);color:#9a6808;border:1px solid rgba(200,136,16,0.4);}
    .badge-movie  {display:inline-block;padding:2px 9px;border-radius:999px;font-size:11px;font-weight:700;background:rgba(216,64,64,0.15);color:#a82828;border:1px solid rgba(216,64,64,0.4);}
    .ep-title-watched {text-decoration: line-through; opacity: 0.45;}
    .star-rating {color:#f0b820; font-size:13px;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# EPISODE TITLES — NARUTO ORIGINAL (220 eps)
# ─────────────────────────────────────────────────────────────────
EP_TITLES_N = {
    1:"Enter: Naruto Uzumaki!", 2:"My Name is Konohamaru!", 3:"Sasuke and Sakura: Friends or Foes?",
    4:"Pass or Fail: Survival Test", 5:"You Failed! Kakashi's Final Decision", 6:"A Dangerous Mission!",
    7:"The Assassin of the Mist!", 8:"The Oath of Pain", 9:"Kakashi: Sharingan Warrior!",
    10:"The Forest of Chakra", 11:"The Land Where a Hero Once Lived", 12:"Battle on the Bridge! Zabuza Returns!",
    13:"Haku's Secret Jutsu: Crystal Ice Mirrors", 14:"The Number One Hyperactive, Knucklehead Ninja Joins the Fight!!",
    15:"Zero Visibility: The Sharingan Shatters", 16:"The Broken Seal", 17:"White Past: Hidden Ambition",
    18:"The Weapons Known as Shinobi", 19:"The Demon in the Snow",
    20:"A New Chapter Begins: The Chunin Exam!", 21:"Identify Yourself: Powerful New Rivals",
    22:"Chunin Challenge: Rock Lee vs. Sasuke!", 23:"Genin Takedown! All Nine Rookies Face Off!",
    24:"Start Your Engines: The Chunin Exam Begins!", 25:"The Tenth Question: All or Nothing!",
    26:"Special Report: Live from the Forest of Death!", 27:"The Chunin Exam Stage 2: The Forest of Death",
    28:"Eat or Be Eaten: Panic in the Forest", 29:"Naruto's Counterattack: Never Give In!",
    30:"The Sharingan Revived: Dragon-Flame Jutsu!", 31:"Bushy Brow's Jutsu: Sasuke Style!",
    32:"Sakura Blossoms!", 33:"Battle Formation: Ino-Shika-Cho!",
    34:"Akamaru Trembles: Gaara's Cruel Strength!", 35:"The Scroll's Secret: No Peeking Allowed",
    36:"Clone vs. Clone: Mine are Better than Yours!", 37:"Surviving the Cut! The Rookie Nine Together Again!",
    38:"Narrowing the Field: Sudden Death Elimination!", 39:"Bushy Brow's Jealousy: Lions Barrage Unleashed!",
    40:"Kakashi and Orochimaru: Face-to-Face!", 41:"Rivals: Spoiling Each Other's Fun",
    42:"The Ultimate Battle: Cha!", 43:"Killer Kunoichi and a Shaky Shikamaru",
    44:"Akamaru Unleashed! Who's Top Dog Now?", 45:"Surprise Attack! Naruto's Secret Weapon!",
    46:"Byakugan Battle: Hinata Grows Bold!", 47:"A Failure Stands Tall!",
    48:"Gaara vs. Rock Lee: The Power of Youth Explodes!", 49:"Lee's Hidden Strength: Forbidden Secret Jutsu!",
    50:"The Fifth Gate: A Splendid Ninja is Born", 51:"A Shadow in Darkness: Danger Approaches Sasuke",
    52:"The Chunin Exam Begins!", 53:"Long Time No See: Jiraiya Returns!",
    54:"The Summoning Jutsu: Wisdom of the Toad Sage!", 55:"A Feeling of Yearning, a Flower Full of Hope",
    56:"Live or Die! Risk It All to Win It All!", 57:"He Flies! He Jumps! He Lurks! Chief Toad Appears!",
    58:"Hospital Besieged: The Evil Hand Revealed!", 59:"The Final Rounds: Rush to the Battle Arena!",
    60:"Byakugan vs. Shadow Clone Jutsu!", 61:"Ultimate Defense: Zero Blind Spot!",
    62:"A Failure's True Power", 63:"Hit It or Quit It: The Final Rounds Begin!",
    64:"Zero Motivation: The Guy with Cloud Envy!", 65:"Dancing Leaf, Squirming Sand",
    66:"Too Late for Help", 67:"Late for the Show, but Ready to Fight: Naruto vs. Sasuke!",
    68:"Zero Hour! The Destruction of the Hidden Leaf Village Begins!", 69:"Village in Distress: A New A-Ranked Mission!",
    70:"A Shirker's Call to Action: A Layabout No More!", 71:"An Unrivaled Match: Hokage Battle Royale!",
    72:"A Mistake from the Past: A Face Revealed!", 73:"Forbidden Secret Technique: Reaper Death Seal!",
    74:"Astonishing Truth! Gaara's Identity Emerges!", 75:"Sasuke's Decision: Pushed to the Edge!",
    76:"Assassin of the Moonlit Night", 77:"Light vs. Dark: The Two Faces of Gaara",
    78:"Explosion! These Are the Naruto!", 79:"Beyond the Limit of Darkness and Light",
    80:"The Third Hokage, Forever...",
    81:"Return of the Morning Mist", 82:"Eye to Eye: Sharingan vs. Sharingan!",
    83:"Jiraiya: Naruto's Potential Disaster!", 84:"Inner Sakura's Hostility: The Enter Intruders!",
    85:"Hate Among the Uchihas: The Last of the Clan!", 86:"Training Begins: I Will Be Strong!",
    87:"Keep on Training: Pop Goes the Water Balloon!", 88:"Focal Point: The Mark of the Leaf",
    89:"An Impossible Choice: The Pain Within Tsunade's Heart", 90:"Unforgivable! A Total Lack of Respect!",
    91:"Kidnapped! Naruto's Hot Spring Adventure!", 92:"Whirlpool of Emotions! What Will Happen to Hinata?",
    93:"Hot-Blooded Confrontation: Student vs. Sensei", 94:"Eat or Die! Mushrooms from Hell!",
    95:"The Third Everyone's Memories", 96:"Deadlock! Sannin Showdown!",
    97:"Kidnapped! Naruto's Hot Spring Adventure!", 98:"Tsunade's Determination",
    99:"The Will of Fire Still Burns!", 100:"Sensei and Student: The Bond of the Shinobi",
    101:"Want to Look, Know and Confirm Kakashi-Sensei's Face",
    102:"Mission: Help an Old Friend in the Land of Tea", 103:"The Race Is On! Trouble on the High Seas!",
    104:"Run Idate Run! Nagi Island Awaits!", 105:"A Fierce Battle of Rolling Thunder!",
    106:"The Last Leg: A Final Act of Desperation",
    107:"The Battle Begins: Naruto vs. Sasuke", 108:"Bitter Rivals and Broken Bonds",
    109:"An Invitation from the Sound", 110:"Formation! The Sasuke Retrieval Squad!",
    111:"Sound vs. Leaf", 112:"Squad Mutiny: Everything Falls Apart!",
    113:"Full Throttle Power! Choji, Ablaze!", 114:"Goodbye Old Friend...! I'll Always Believe in You!",
    115:"Your Opponent is Me!", 116:"360 Degrees of Vision: The Byakugan's Blind Spot!",
    117:"Losing is Not an Option!", 118:"The Vessel Arrives Too Late",
    119:"Miscalculation: A New Enemy Appears!", 120:"Roar and Howl! The Ultimate Tag-Team!",
    121:"To Each His Own Battle", 122:"Fakeout: Shikamaru's Comeback!",
    123:"The Leaf's Handsome Devil!", 124:"The Beast Within",
    125:"The Sand Shinobi: Allies of the Leaf", 126:"Showdown: Gaara vs. Kimimaro!",
    127:"Vengeful Strike! The Brazen Blade!", 128:"A Cry on Deaf Ears",
    129:"Brothers: Distance Among the Uchiha", 130:"Father and Son, the Broken Crest",
    131:"The Secrets of the Mangekyō Sharingan!", 132:"For a Friend",
    133:"A Plea from a Friend", 134:"The End of Tears",
    135:"The Promise That Could Not Be Kept",
    136:"Deep Cover?! A Super S-Ranked Mission!", 137:"A Town of Outlaws: The Shadow of the Fuma Clan",
    138:"Pure Betrayal, and a Fleeting Plea!", 139:"Pure Terror! The House of Orochimaru",
    140:"Two Idols Risking Their Lives: The Way a Shinobi Dies",
    141:"Reunion, and Then the Journey Onwards!", 142:"The Three Villains from the Maximum Security Prison",
    143:"Tonton! I'm Counting on You!", 144:"A New Squad! Two People and a Dog?!",
    145:"A New Formation: Ino-Shika-Cho!", 146:"Remaining Ambition: Orochimaru's Shadow",
    147:"A Clash of Fate: You Can't Bring Me Down!", 148:"The Search for the Rare Bikōchū Beetle",
    149:"What's the Difference? Don't All Insects Look Alike?",
    150:"A Battle of Bugs! The Deceivers and the Deceived!",
    151:"Blaze Away, Byakugan! This Is My Ninja Way!",
    152:"Funeral March for the Living", 153:"A Lesson Learned: The Iron Fist of Love!",
    154:"The Enemy of the Byakugan", 155:"The Dark Creeping Clouds",
    156:"Raiga's Counterattack", 157:"Run! The Curry of Life!",
    158:"Follow My Lead! The Great Survival Challenge", 159:"The Bounty Hunter from the Wilderness",
    160:"Hunt or Be Hunted?! Showdown at the O.K. Temple!", 161:"The Appearance of Strange Visitors",
    162:"The Cursed Warrior", 163:"The Tactician's Intent", 164:"Too Late for Help",
    165:"The Death of Naruto", 166:"When Time Stands Still",
    167:"When Egrets Flap Their Wings",
    168:"Mix It, Stretch It, Boil It Up! Burn Copper Pot, Burn!",
    169:"Remembrance: The Lost Page", 170:"The Closed Door",
    171:"Infiltration: The Set-Up!", 172:"Despair: A Fractured Heart",
    173:"Battle at Sea: The Power Unleashed!", 174:"Impossible! Celebrity Ninja Art: Money Style Jutsu!",
    175:"The Treasure Hunt Is On!",
    176:"Run, Dodge, Zigzag! Chase or Be Chased!", 177:"Please, Mr. Postman!",
    178:"Encounter! The Boy with a Star's Name", 179:"The Remembered Lullaby",
    180:"Hidden Jutsu! The Price of Ninja Art: Kujaku", 181:"Hoshikage: The Buried Truth",
    182:"Reunion: The Remaining Time", 183:"The Star's Radiance", 184:"Kiba's Long Day",
    185:"A Legend from the Hidden Leaf: The Onbaa!", 186:"Laughing Shino",
    187:"Open for Business! The Leaf Moving Service", 188:"The Mystery of the Targeted Merchants",
    189:"A Limitless Supply of Ninja Tools", 190:"The Byakugan Sees the Blind Spot!",
    191:"Forecast: Death! Cloudy with Chance of Sun!", 192:"Ino Screams! Chubby Paradise!",
    193:"Viva Dojo Challenge! Youth Is All About Passion!", 194:"The Mysterious Curse of the Haunted Castle",
    195:"The Third Super-Beast!", 196:"Hot-Blooded Confrontation: Student vs. Sensei",
    197:"Crisis: The Hidden Leaf 11 Gather!", 198:"The Anbu Gives Up? Naruto's Recollection",
    199:"The Missed Target", 200:"The Powerful Helper",
    201:"Multiple Traps! Countdown to Destruction", 202:"The Top 5 Ninja Battles!",
    203:"Kurenai's Decision: Team 8 Left Behind", 204:"Yakumo's Sealed Power",
    205:"Kurenai's Top Secret Mission: The Promise with the Third Hokage",
    206:"Genjutsu or Reality?", 207:"The Supposed Sealed Ability",
    208:"The Weight of the Prized Artifact!", 209:"The Enemy: Ninja Dropouts",
    210:"The Bewildering Forest", 211:"Memory of Flames", 212:"To Each His Own Path",
    213:"Vanished Memories", 214:"Bringing Back Reality", 215:"A Past to Be Erased",
    216:"The Targeted Shukaku", 217:"Sand Alliance with the Leaf Shinobi",
    218:"Sealed Sand: The Counterattack!", 219:"The Ultimate Weapon Reborn",
    220:"Departure and Arrival",
}

# ─────────────────────────────────────────────────────────────────
# EPISODE TITLES — SHIPPUDEN (500 eps)
# ─────────────────────────────────────────────────────────────────
EP_TITLES_S = {
    1:"Homecoming", 2:"The Akatsuki Makes Its Move", 3:"The Results of Training",
    4:"The Jinchuriki of the Sand", 5:"The Kazekage Stands Tall", 6:"Mission Cleared!",
    7:"Run, Kankuro", 8:"Team Kakashi, Deployed", 9:"The Jinchuriki's Tears",
    10:"Sealing Jutsu: Nine Phantoms", 11:"The Medical Ninja's Student",
    12:"The Retired Granny's Determination", 13:"A Meeting With Destiny",
    14:"Naruto's Growth", 15:"The Secret Weapon is Called...", 16:"The Secret of Jinchuriki",
    17:"The Death of Gaara!", 18:"Charge Tactic! Button Hook Entry!!",
    19:"Traps Activate! Team Guy's Enemy", 20:"Hiruko vs. Two Kunoichi!",
    21:"Sasori's Real Face", 22:"Chiyo's Secret Skills", 23:"Father and Mother",
    24:"The Third Kazekage", 25:"Three Minutes Between Life and Death",
    26:"Puppet Fight: 10 vs. 100!", 27:"Impossible Dream", 28:"Beasts! Foolish Beasts!",
    29:"Kakashi Enlightened!", 30:"Aesthetics of an Instant", 31:"The Legacy!",
    32:"Return of the Kazekage", 33:"The New Target", 34:"Bonds", 35:"The Vessel",
    36:"The Fake Smile", 37:"Untitled", 38:"Simulation", 39:"The Tenchi Bridge",
    40:"Nine-Tails Unleashed", 41:"The Top-Secret Mission Begins",
    42:"Orochimaru vs. Jinchuriki", 43:"Sakura's Determination",
    44:"The Secret of the Battle!", 45:"An Eternal Battle!?", 46:"The Unfinished Page",
    47:"Infiltration: The Den of the Snake!", 48:"Bonds", 49:"Something Important…",
    50:"The Picture Book's Story", 51:"Reunion", 52:"The Power of Uchiha", 53:"Title",
    54:"Nightmare", 55:"Wind", 56:"Writhing", 57:"Deception",
    58:"The Man Who Knows the Truth", 59:"A New Enemy", 60:"Impermanence",
    61:"Contact", 62:"Teammate", 63:"The Two Kings", 64:"Jet-Black Signal Fire",
    65:"Lockdown of Darkness", 66:"Confessions", 67:"Everyone's Struggle to the Death",
    68:"Moment of Awakening", 69:"Despair", 70:"Resonance", 71:"My Friend",
    72:"The Quietly Approaching Threat", 73:"Akatsuki's Invasion",
    74:"Under the Starry Sky",
    75:"Tales of a Gutsy Ninja: Jiraiya Ninja Scrolls — Part 1",
    76:"Tales of a Gutsy Ninja: Jiraiya Ninja Scrolls — Part 2",
    77:"The Whirlpool Country Shinobi — Uzumaki Naruto!", 78:"The Reversed Seal",
    79:"The Mystery of Tobi", 80:"Searching for the Forbidden Word", 81:"Sad News",
    82:"Team 10", 83:"Target: Nine-Tails", 84:"Judgment", 85:"The Terrifying Secret",
    86:"Ao's Chase", 87:"The Rogue Ninja Mukade!", 88:"Approaching Shadows",
    89:"The Price of Power", 90:"A Shinobi's Determination",
    91:"Orochimaru's Hideout Discovered", 92:"Encounter",
    93:"Connecting Hearts", 94:"A Night of Rain", 95:"The Two Charms",
    96:"The Unseeing Enemy", 97:"The Labyrinth of Distorted Reflection",
    98:"The Target Appears", 99:"The Rampaging Tailed Beast",
    100:"Inside the Mist", 101:"Everyone's Feelings", 102:"Regroup!",
    103:"The Four-Corner Sealing Barrier", 104:"Breaking the Crystal Style",
    105:"The Battle Over the Barrier", 106:"Red Camellia",
    107:"Strange Bedfellows", 108:"Guidepost of the Camellia",
    109:"Counterattack of the Curse Mark", 110:"Memory of Guilt",
    111:"Shattered Promise", 112:"A Place to Return To",
    113:"The Serpent's Pupil", 114:"Eye of a Hawk",
    115:"Zabuza's Blade", 116:"Guardian of the Iron Wall",
    117:"Jugo of the Northern Hideout", 118:"Formation!",
    119:"Kakashi Chronicles: A Boy's Life on the Battlefield, Part 1",
    120:"Kakashi Chronicles: A Boy's Life on the Battlefield, Part 2",
    121:"Assemble", 122:"The Hunt", 123:"Clash!", 124:"Art",
    125:"Disappearance", 126:"Twilight",
    127:"Tales of a Gutsy Ninja ~Jiraiya Ninja Scroll~ Part 1",
    128:"Tales of a Gutsy Ninja ~Jiraiya Ninja Scroll~ Part 2",
    129:"Infiltrate! The Village Hidden in the Rain",
    130:"The Man Who Became God", 131:"Honoured Sage Mode!",
    132:"In Attendance, the Six Paths of Pain",
    133:"The Tale of Jiraiya the Gallant", 134:"Banquet Invitation",
    135:"The Longest Moment",
    136:"The Light and Dark of the Mangekyō Sharingan",
    137:"Amaterasu!", 138:"The End", 139:"The Mystery of Tobi",
    140:"Fate", 141:"Truth",
    142:"Battle of Valley of Clouds and Lightning",
    143:"The Eight-Tails vs. Sasuke",
    144:"Wanderer", 145:"Successor of the Forbidden Jutsu",
    146:"The Successor's Wish", 147:"Rogue Ninja's Past",
    148:"Heir to Darkness", 149:"Separation",
    150:"The Forbidden Jutsu Released", 151:"Master and Student",
    152:"Somber News", 153:"Following the Master's Shadow", 154:"Decryption",
    155:"The First Challenge", 156:"Surpassing the Master",
    157:"Assault on the Leaf Village!", 158:"Power to Believe",
    159:"Pain vs. Kakashi", 160:"Mystery of Pain",
    161:"Surname Is Sarutobi! Given Name, Konohamaru!", 162:"Pain to the World",
    163:"Explode! Sage Mode", 164:"Danger! Sage Mode Limit Reached",
    165:"Nine-Tails, Captured!", 166:"Confession", 167:"Planetary Devastation",
    168:"The Fourth Hokage", 169:"The Two Students",
    170:"Big Adventure! The Quest for the Fourth Hokage's Legacy — Part 1",
    171:"Big Adventure! The Quest for the Fourth Hokage's Legacy — Part 2",
    172:"Meeting", 173:"The Origin of Pain", 174:"Naruto's Plea",
    175:"Hero of the Hidden Leaf",
    176:"Rookie Instructor Iruka", 177:"Iruka's Ordeal",
    178:"Iruka's Decision", 179:"Kakashi Hatake, the Jonin in Charge",
    180:"Inari's Courage Put to the Test", 181:"Naruto's School of Revenge",
    182:"Gaara's Bond", 183:"Naruto: Outbreak", 184:"Deploy! Team Tenten",
    185:"Animal District", 186:"Ah, the Medicine of Youth",
    187:"Gutsy Master and Student: The Training",
    188:"Record of the Ninja Gutsy Master and Student",
    189:"Sasuke's Paw Encyclopedia", 190:"Naruto and the Old Soldier",
    191:"Kakashi Love Song", 192:"Neji Chronicles",
    193:"The Man Who Died Twice", 194:"The Worst Three-Legged Race",
    195:"Team 10's Teamwork", 196:"Drive Towards Darkness",
    197:"The Sixth Hokage Danzo", 198:"Five Kage Summit's Eve",
    199:"Enter the Five Kage!", 200:"Naruto's Plea", 201:"Madara Uchiha",
    202:"Racing Lightning", 203:"Sasuke's Ninja Way",
    204:"Power of the Five Kage!", 205:"Declaration of War",
    206:"Sakura's Feelings", 207:"The Tailed Beast vs. The Tailless Tailed Beast",
    208:"As One's Friend", 209:"Danzo's Right Arm",
    210:"The Forbidden Visual Jutsu", 211:"Danzo Shimura",
    212:"Sakura's Resolve", 213:"Lost Bonds", 214:"The Burden",
    215:"Two Fates", 216:"High-Level Shinobi",
    217:"The Island Turtle Appears!", 218:"A Boat to Live On",
    219:"Paradox", 220:"Killer Bee and Motoi", 221:"The Ace in the Hole",
    222:"The Five Great Nations Mobilize",
    223:"The Young Man and the Sea", 224:"The Ninja of Benisu",
    225:"The Cursed Ghost Ship", 226:"Battleship Island",
    227:"The Forgotten Island", 228:"Fight! Rock Lee!",
    229:"Eat or Die! Mushrooms from Hell!",
    230:"Revenge of the Shadow Clones", 231:"The Closed Route",
    232:"The Girls' Get-Together", 233:"Naruto's Imposter",
    234:"Naruto's Favorite Student", 235:"The Kunoichi of Nadeshiko Village",
    236:"Friends You Can Count On",
    237:"Ah, My Hero Lady Tsunade!", 238:"Sai's Day Off",
    239:"The Legendary Ino-Shika-Cho Trio",
    240:"Kiba's Determination", 241:"Kakashi, My Eternal Rival!",
    242:"Naruto's Vow",
    243:"Land Ahoy! Is this the Paradise Island?",
    244:"Battleship Island!", 245:"The Terrifying Experiment",
    246:"Ah, My Hero Lady Tsunade!", 247:"Target: Kurosuki Family Removal Mission",
    248:"Obito and Rin", 249:"As a Taijutsu User",
    250:"Battle in Paradise! Odd Beast vs. The Monster!",
    251:"The Man Named Kisame", 252:"The Angelic Herald of Death",
    253:"The Bridge to Peace", 254:"The Super Secret S-Rank Mission",
    255:"Power — Episode 1", 256:"Power — Episode 2",
    257:"Meeting", 258:"The Beginning of the Battle", 259:"Rift", 260:"Qualified",
    261:"For My Friend", 262:"War Begins!", 263:"Sai and Shin",
    264:"The Secret of the Four-Eyes", 265:"Partners",
    266:"The First and Last Opponent",
    267:"The Brilliant Military Advisor of the Hidden Leaf",
    268:"Battleground!", 269:"Forbidden Words", 270:"Golden Bonds",
    271:"Road to Sakura", 272:"Mifune vs. Hanzo", 273:"True Kindness",
    274:"The Complete Ino-Shika-Cho Formation!", 275:"A Message from the Heart",
    276:"Attack! Fury of the Rasengan!", 277:"Climb up! Rock Lee",
    278:"Secrets of the Reanimation Jutsu", 279:"White Zetsu's Trap",
    280:"Aesthetics of an Instant", 281:"The Allied Mom Force!!",
    282:"The Pa and the Ma", 283:"Two Suns",
    284:"The Helmet Splitter: Jinin Akebino!",
    285:"User of the Scorch Style: Pakura of the Sand!",
    286:"Things You Can't Get Back", 287:"One Worth Betting On",
    288:"Danger: Jinpachi and Kushimaru!",
    289:"The Lightning Blade: Ameyuri Ringo!",
    290:"Power — Episode 1", 291:"Power — Episode 2",
    292:"Power — Episode 3", 293:"Power — Episode 4",
    294:"Power — Episode 5", 295:"Power — Episode Final",
    296:"Naruto Enters the Battle!", 297:"A Father's Hope, A Mother's Love",
    298:"Contact with the Nine-Tails", 299:"The Acknowledged One",
    300:"The Steam Imp", 301:"Paradox", 302:"Terror: The Steam Imp",
    303:"Ghosts from the Past", 304:"The Underworld Transfer Jutsu",
    305:"The Vengeful", 306:"The Heart's Eye", 307:"Fade into the Moonlight",
    308:"Crescent Moon Dance", 309:"An A-Rank Mission: The Contest",
    310:"The Ninja of Benisu", 311:"Prologue of Road to Ninja",
    312:"The Old Master and the Dragon's Eye",
    313:"Rain Followed by Snow, with Some Lightning",
    314:"The Sad Sun Shower", 315:"Lingering Snow",
    316:"The Reanimated Allied Forces", 317:"Shino vs. Torune!",
    318:"A Hole in the Heart: The Other Jinchuriki",
    319:"The Soul That Dwells in a Puppet", 320:"Risking It All to Win",
    321:"Reinforcements Arrive", 322:"Madara Uchiha",
    323:"The Risks of Edo Tensei",
    324:"The Unbreakable Mask and the Shattered Bubble",
    325:"Jinchuriki vs. Jinchuriki!!", 326:"Four Tails, the King of Sage Monkeys",
    327:"Nine-Tails", 328:"Kurama", 329:"Two-Man Team",
    330:"The Promise of Victory", 331:"Eyes That See in the Dark",
    332:"A Will of Stone", 333:"The Three-Minute Limit",
    334:"The Risks of Edo Tensei", 335:"To Each Their Own Leaf",
    336:"Mysterious Masked Man", 337:"Izanagi and Izanami",
    338:"Izanami Activated!", 339:"I Will Love You Always",
    340:"Reanimation Jutsu: Release!", 341:"Orochimaru's Return",
    342:"The Secret of the Transportation Technique",
    343:"Who Are You?", 344:"Obito and Madara", 345:"I'm in Hell",
    346:"World of Dreams", 347:"Creeping Shadow",
    348:"The New Tailed Beast-Bomb",
    349:"A Hole in the Heart: The Other Jinchuriki",
    350:"Minato's Death", 351:"The Sage of Six Paths",
    352:"The Eternal Kaleidoscope", 353:"Jugo's Long Travels",
    354:"The New Three-Way Deadlock", 355:"Kakashi's Resolve",
    356:"The Directive to Take the Nine-Tails", 357:"An Opening",
    358:"The Mask Crumbles", 359:"Obito Uchiha",
    360:"Ninja Alliance — Shattered!", 361:"Kakashi's Conclusion",
    362:"The Allied Shinobi Forces Technique", 363:"The Ties That Bind",
    364:"Those Who Dance in the Shadows", 365:"The All-Knowing",
    366:"Hashirama and Madara", 367:"Warring States Period",
    368:"My True Dream", 369:"Sasuke's Answer", 370:"Hole",
    371:"Something to Fill the Hole", 372:"Team 7 Assemble!",
    373:"The New Three-Way Deadlock", 374:"Kakashi vs. Obito",
    375:"The Directive to Take the Nine-Tails!",
    376:"Naruto vs. Mecha Naruto", 377:"The Jinchuriki of the Ten Tails",
    378:"An Opening", 379:"The Adored Elder Sister",
    380:"The Day Naruto Was Born", 381:"The Exploding Human",
    382:"A Fabricated Past", 383:"Pursuing Hope",
    384:"A Heart Filled with Coexistence", 385:"Obito Uchiha",
    386:"I'm Always Watching", 387:"The Promise That Was Kept",
    388:"My Will Is", 389:"The Adored Elder Sister",
    390:"Hanabi's Decision", 391:"Madara Uchiha Returns",
    392:"The Hidden Heart", 393:"A True Ending",
    394:"The New Chunin Exams", 395:"The Chunin Exams Begin",
    396:"The Three Questions", 397:"One Worthy as a Leader",
    398:"The Night Before the Second Exam",
    399:"Demon Desert Survival", 400:"As a Taijutsu User",
    401:"The Ultimate", 402:"Escape vs. Pursuit",
    403:"Unwavering Gutsiness", 404:"Tenten's Troubles",
    405:"The Imprisoned Pair", 406:"The Place Where I Belong",
    407:"The Yamanaka Clan: Secret Ninjutsu", 408:"The Cursed Puppet",
    409:"Their Backs", 410:"The Hidden Plot Set Into Motion",
    411:"The Targeted Tailed Beast", 412:"Neji's Judgment",
    413:"Hopes Entrusted to the Future",
    414:"One Heart", 415:"The Two Mangekyo",
    416:"The Formation of Team Minato", 417:"The Dual Uchiha",
    418:"The Blue Beast vs. Six Paths Madara",
    419:"Overflowing Light", 420:"The Eight Inner Gates Formation",
    421:"The Allied Shinobi Forces Jutsu",
    422:"The Sage of Six Paths", 423:"The Ones Who Will Inherit",
    424:"To Rise Up", 425:"Naruto and Sasuke",
    427:"To the Dreamworld", 428:"Where Tenten Belongs",
    429:"Killer B Rappuden: Part 1", 430:"Killer B Rappuden: Part 2",
    431:"To See That Smile, Just One More Time",
    432:"The Loser Ninja", 433:"The Search Mission",
    434:"Team Jiraiya", 435:"Order of Priority",
    436:"The Masked Man", 437:"The Sealed Power",
    438:"The Rules or a Comrade", 439:"The Child of Prophecy",
    440:"The Caged Bird", 441:"Returning Home",
    442:"The Mutual Path", 443:"The Difference in Power",
    444:"Leaving the Village", 445:"Pursuers",
    446:"Collision", 447:"Another Moon",
    448:"Comrade", 449:"The Shinobi Unite", 450:"Rival",
    451:"Birth and Death", 452:"The Genius", 453:"The Pain of Living",
    454:"Shisui's Request", 455:"Moonlit Night",
    456:"The Darkness of the Akatsuki", 457:"Partner",
    458:"The Ten-Tails' Jinchuriki", 459:"She of the Beginning",
    460:"Kaguya's Dimensions", 461:"Orochimaru's Test Subjects",
    462:"The Genius", 463:"The Sharingan Revived",
    464:"Ninshu: The Ninja Creed", 465:"The Ninshu World",
    466:"The Reason for Reincarnation",
    467:"You'll Be My Backup", 468:"The Seal of Reconciliation",
    469:"Connecting Thoughts", 470:"The Two of Them… Always",
    471:"You Better...", 472:"The Sharingan Revived",
    473:"Congratulations", 474:"The Valley of the End",
    475:"The Final Battle", 476:"Naruto and Sasuke",
    477:"The Unison Sign", 478:"Naruto Uzumaki!!",
    479:"Naruto and Hinata",
    480:"Naruto Uzumaki!!", 481:"Sasuke Uchiha!!", 482:"Sakura Uchiha!!",
    483:"Gaara and Shukaku", 484:"Sai and Shin",
    485:"Sasuke's Story — Sunrise Part 1", 486:"Sasuke's Story — Sunrise Part 2",
    487:"Shikamaru's Story Part 1", 488:"Shikamaru's Story Part 2",
    489:"Shikamaru's Story Part 3", 490:"Temari's Story",
    491:"Konoha Hiden Part 1", 492:"Konoha Hiden Part 2",
    493:"Konoha Hiden Part 3", 494:"The Last Mission",
    495:"Wedding Invitation", 496:"Cloudy with Chance of Tears",
    497:"The Night Before the Wedding", 498:"The Outcome of the Vote",
    499:"Connecting Feelings", 500:"The Message",
}

# ─────────────────────────────────────────────────────────────────
# IMDB RATINGS
# ─────────────────────────────────────────────────────────────────
EP_RATINGS = {
    "naruto-1":7.9,"naruto-2":7.0,"naruto-3":7.2,"naruto-4":7.8,"naruto-5":8.0,
    "naruto-6":7.3,"naruto-7":7.7,"naruto-8":7.9,"naruto-9":7.9,"naruto-10":7.1,
    "naruto-11":7.1,"naruto-12":7.3,"naruto-13":7.7,"naruto-14":7.1,"naruto-15":7.6,
    "naruto-16":8.4,"naruto-17":8.2,"naruto-18":8.0,"naruto-19":9.1,"naruto-20":6.9,
    "naruto-21":7.2,"naruto-22":7.5,"naruto-23":7.2,"naruto-24":7.8,"naruto-25":7.9,
    "naruto-26":4.3,"naruto-27":7.3,"naruto-28":8.0,"naruto-29":8.2,"naruto-30":8.5,
    "naruto-31":7.6,"naruto-32":7.9,"naruto-33":8.2,"naruto-34":7.7,"naruto-35":7.0,
    "naruto-36":7.4,"naruto-37":6.8,"naruto-38":7.3,"naruto-39":7.8,"naruto-40":7.5,
    "naruto-41":6.5,"naruto-42":6.7,"naruto-43":7.4,"naruto-44":7.7,"naruto-45":7.9,
    "naruto-46":7.7,"naruto-47":8.1,"naruto-48":9.3,"naruto-49":9.0,"naruto-50":9.3,
    "naruto-51":7.2,"naruto-52":6.8,"naruto-53":7.4,"naruto-54":7.3,"naruto-55":7.0,
    "naruto-56":7.7,"naruto-57":7.6,"naruto-58":7.6,"naruto-59":6.8,"naruto-60":7.6,
    "naruto-61":7.9,"naruto-62":8.8,"naruto-63":7.3,"naruto-64":8.2,"naruto-65":7.1,
    "naruto-66":7.9,"naruto-67":8.3,"naruto-68":8.1,"naruto-69":7.9,"naruto-70":7.7,
    "naruto-71":8.5,"naruto-72":8.3,"naruto-73":8.0,"naruto-74":8.0,"naruto-75":7.9,
    "naruto-76":8.2,"naruto-77":8.0,"naruto-78":9.1,"naruto-79":9.2,"naruto-80":8.7,
    "naruto-81":8.0,"naruto-82":8.4,"naruto-83":7.7,"naruto-84":8.7,"naruto-85":8.1,
    "naruto-86":7.1,"naruto-87":7.2,"naruto-88":7.3,"naruto-89":7.2,"naruto-90":7.8,
    "naruto-91":7.6,"naruto-92":7.6,"naruto-93":8.1,"naruto-94":8.7,"naruto-95":8.4,
    "naruto-96":8.3,"naruto-97":6.2,"naruto-98":7.1,"naruto-99":6.7,"naruto-100":7.7,
    "naruto-101":7.4,"naruto-102":6.4,"naruto-103":6.3,"naruto-104":6.5,"naruto-105":6.7,
    "naruto-106":6.7,"naruto-107":8.2,"naruto-108":7.9,"naruto-109":8.1,"naruto-110":8.0,
    "naruto-111":7.7,"naruto-112":7.7,"naruto-113":7.7,"naruto-114":8.7,"naruto-115":7.8,
    "naruto-116":8.0,"naruto-117":8.8,"naruto-118":7.6,"naruto-119":7.6,"naruto-120":7.5,
    "naruto-121":7.5,"naruto-122":7.9,"naruto-123":8.0,"naruto-124":8.9,"naruto-125":8.4,
    "naruto-126":8.3,"naruto-127":8.3,"naruto-128":8.0,"naruto-129":8.1,"naruto-130":7.8,
    "naruto-131":8.0,"naruto-132":9.0,"naruto-133":9.5,"naruto-134":9.2,"naruto-135":8.2,
    "naruto-136":6.4,"naruto-137":6.5,"naruto-138":6.5,"naruto-139":6.9,"naruto-140":6.8,
    "naruto-141":6.9,"naruto-142":6.2,"naruto-143":6.2,"naruto-144":6.0,"naruto-145":6.2,
    "naruto-146":6.2,"naruto-147":6.4,"naruto-148":6.8,"naruto-149":6.9,"naruto-150":6.7,
    "naruto-151":7.1,"naruto-152":6.2,"naruto-153":6.1,"naruto-154":6.3,"naruto-155":6.1,
    "naruto-156":6.0,"naruto-157":6.4,"naruto-158":6.3,"naruto-159":6.1,"naruto-160":5.9,
    "naruto-161":5.4,"naruto-162":5.7,"naruto-163":5.9,"naruto-164":5.9,"naruto-165":6.2,
    "naruto-166":6.1,"naruto-167":5.9,"naruto-168":5.7,"naruto-169":6.5,"naruto-170":6.4,
    "naruto-171":6.4,"naruto-172":6.3,"naruto-173":6.7,"naruto-174":5.0,"naruto-175":6.2,
    "naruto-176":6.2,"naruto-177":5.9,"naruto-178":5.9,"naruto-179":5.9,"naruto-180":6.1,
    "naruto-181":6.0,"naruto-182":6.2,"naruto-183":6.0,"naruto-184":5.8,"naruto-185":5.9,
    "naruto-186":6.1,"naruto-187":5.8,"naruto-188":5.7,"naruto-189":5.9,"naruto-190":6.4,
    "naruto-191":5.8,"naruto-192":5.5,"naruto-193":6.1,"naruto-194":5.6,"naruto-195":6.4,
    "naruto-196":6.5,"naruto-197":6.6,"naruto-198":6.8,"naruto-199":7.0,"naruto-200":7.0,
    "naruto-201":7.3,"naruto-202":4.6,"naruto-203":6.2,"naruto-204":6.3,"naruto-205":6.4,
    "naruto-206":6.5,"naruto-207":6.6,"naruto-208":5.3,"naruto-209":5.9,"naruto-210":6.1,
    "naruto-211":6.0,"naruto-212":6.1,"naruto-213":6.3,"naruto-214":6.3,"naruto-215":6.7,
    "naruto-216":7.1,"naruto-217":7.2,"naruto-218":7.3,"naruto-219":7.2,"naruto-220":8.0,
    "shippuden-1":8.2,"shippuden-2":7.8,"shippuden-3":7.9,"shippuden-4":8.1,"shippuden-5":8.1,
    "shippuden-6":8.1,"shippuden-7":7.6,"shippuden-8":7.6,"shippuden-9":7.5,"shippuden-10":7.4,
    "shippuden-11":7.6,"shippuden-12":7.8,"shippuden-13":8.0,"shippuden-14":8.3,"shippuden-15":8.3,
    "shippuden-16":7.5,"shippuden-17":7.6,"shippuden-18":7.5,"shippuden-19":7.5,"shippuden-20":7.9,
    "shippuden-21":7.9,"shippuden-22":7.7,"shippuden-23":7.7,"shippuden-24":7.9,"shippuden-25":7.7,
    "shippuden-26":8.8,"shippuden-27":8.5,"shippuden-28":6.8,"shippuden-29":8.0,"shippuden-30":8.3,
    "shippuden-31":8.8,"shippuden-32":7.7,"shippuden-33":7.4,"shippuden-34":7.1,"shippuden-35":7.1,
    "shippuden-36":6.9,"shippuden-37":6.9,"shippuden-38":6.9,"shippuden-39":7.7,"shippuden-40":7.6,
    "shippuden-41":8.0,"shippuden-42":8.5,"shippuden-43":7.8,"shippuden-44":7.2,"shippuden-45":7.1,
    "shippuden-46":7.1,"shippuden-47":7.3,"shippuden-48":7.1,"shippuden-49":7.3,"shippuden-50":7.2,
    "shippuden-51":7.4,"shippuden-52":7.9,"shippuden-53":7.4,"shippuden-54":7.3,"shippuden-55":7.7,
    "shippuden-56":7.3,"shippuden-57":6.6,"shippuden-58":6.3,"shippuden-59":6.2,"shippuden-60":6.5,
    "shippuden-61":6.5,"shippuden-62":6.4,"shippuden-63":6.4,"shippuden-64":6.4,"shippuden-65":6.7,
    "shippuden-66":6.5,"shippuden-67":6.6,"shippuden-68":6.6,"shippuden-69":6.4,"shippuden-70":6.5,
    "shippuden-71":6.4,"shippuden-72":7.2,"shippuden-73":7.5,"shippuden-74":7.3,"shippuden-75":7.1,
    "shippuden-76":7.5,"shippuden-77":8.2,"shippuden-78":8.6,"shippuden-79":8.8,"shippuden-80":9.0,
    "shippuden-81":8.1,"shippuden-82":8.9,"shippuden-83":8.2,"shippuden-84":8.6,"shippuden-85":8.8,
    "shippuden-86":9.1,"shippuden-87":9.2,"shippuden-88":8.9,"shippuden-89":7.5,"shippuden-90":6.7,
    "shippuden-91":6.7,"shippuden-92":6.4,"shippuden-93":6.2,"shippuden-94":6.2,"shippuden-95":6.1,
    "shippuden-96":6.3,"shippuden-97":6.6,"shippuden-98":6.6,"shippuden-99":6.6,"shippuden-100":6.3,
    "shippuden-101":6.2,"shippuden-102":6.2,"shippuden-103":6.6,"shippuden-104":6.7,"shippuden-105":6.3,
    "shippuden-106":6.4,"shippuden-107":6.3,"shippuden-108":6.2,"shippuden-109":6.2,"shippuden-110":6.4,
    "shippuden-111":6.5,"shippuden-112":6.7,"shippuden-113":7.8,"shippuden-114":8.3,"shippuden-115":7.3,
    "shippuden-116":7.0,"shippuden-117":7.1,"shippuden-118":7.1,"shippuden-119":8.9,"shippuden-120":9.5,
    "shippuden-121":7.6,"shippuden-122":7.6,"shippuden-123":8.5,"shippuden-124":8.7,"shippuden-125":8.2,
    "shippuden-126":8.4,"shippuden-127":8.1,"shippuden-128":8.7,"shippuden-129":8.0,"shippuden-130":8.7,
    "shippuden-131":9.0,"shippuden-132":9.2,"shippuden-133":9.7,"shippuden-134":8.2,"shippuden-135":8.4,
    "shippuden-136":9.2,"shippuden-137":9.3,"shippuden-138":9.7,"shippuden-139":8.7,"shippuden-140":9.2,
    "shippuden-141":9.5,"shippuden-142":7.8,"shippuden-143":8.7,"shippuden-144":6.0,"shippuden-145":6.0,
    "shippuden-146":6.1,"shippuden-147":6.1,"shippuden-148":5.9,"shippuden-149":6.1,"shippuden-150":6.2,
    "shippuden-151":6.4,"shippuden-152":8.2,"shippuden-153":8.6,"shippuden-154":7.8,"shippuden-155":7.8,
    "shippuden-156":7.6,"shippuden-157":8.1,"shippuden-158":8.4,"shippuden-159":9.4,"shippuden-160":8.3,
    "shippuden-161":8.4,"shippuden-162":9.4,"shippuden-163":9.4,"shippuden-164":9.5,"shippuden-165":9.5,
    "shippuden-166":9.7,"shippuden-167":9.7,"shippuden-168":9.6,"shippuden-169":8.7,"shippuden-170":5.8,
    "shippuden-171":5.8,"shippuden-172":8.0,"shippuden-173":8.7,"shippuden-174":8.8,"shippuden-175":9.5,
    "shippuden-176":6.7,"shippuden-177":6.6,"shippuden-178":6.7,"shippuden-179":6.4,"shippuden-180":5.8,
    "shippuden-181":5.6,"shippuden-182":6.3,"shippuden-183":5.6,"shippuden-184":5.7,"shippuden-185":4.8,
    "shippuden-186":5.6,"shippuden-187":5.7,"shippuden-188":5.8,"shippuden-189":5.4,"shippuden-190":6.0,
    "shippuden-191":6.1,"shippuden-192":5.8,"shippuden-193":5.9,"shippuden-194":5.9,"shippuden-195":5.6,
    "shippuden-196":5.5,"shippuden-197":7.4,"shippuden-198":7.5,"shippuden-199":7.4,"shippuden-200":7.6,
    "shippuden-201":8.0,"shippuden-202":8.2,"shippuden-203":8.6,"shippuden-204":8.4,"shippuden-205":8.3,
    "shippuden-206":7.3,"shippuden-207":8.2,"shippuden-208":7.7,"shippuden-209":8.7,"shippuden-210":8.6,
    "shippuden-211":8.9,"shippuden-212":6.7,"shippuden-213":6.1,"shippuden-214":7.0,"shippuden-215":7.4,
    "shippuden-216":7.5,"shippuden-217":7.4,"shippuden-218":7.0,"shippuden-219":8.0,"shippuden-220":7.2,
    "shippuden-221":7.8,"shippuden-222":7.1,"shippuden-223":5.6,"shippuden-224":5.3,"shippuden-225":5.2,
    "shippuden-226":4.9,"shippuden-227":5.3,"shippuden-228":5.2,"shippuden-229":5.0,"shippuden-230":5.4,
    "shippuden-231":5.2,"shippuden-232":6.3,"shippuden-233":5.3,"shippuden-234":6.1,"shippuden-235":5.6,
    "shippuden-236":5.6,"shippuden-237":5.9,"shippuden-238":5.7,"shippuden-239":5.8,"shippuden-240":5.6,
    "shippuden-241":6.6,"shippuden-242":6.1,"shippuden-243":7.0,"shippuden-244":7.1,"shippuden-245":8.2,
    "shippuden-246":9.1,"shippuden-247":9.1,"shippuden-248":9.6,"shippuden-249":9.6,"shippuden-250":8.0,
    "shippuden-251":8.4,"shippuden-252":8.2,"shippuden-253":8.8,"shippuden-254":6.6,"shippuden-255":7.3,
    "shippuden-256":8.4,"shippuden-257":5.7,"shippuden-258":5.4,"shippuden-259":5.3,"shippuden-260":5.6,
    "shippuden-261":7.8,"shippuden-262":8.0,"shippuden-263":7.8,"shippuden-264":7.6,"shippuden-265":7.7,
    "shippuden-266":8.0,"shippuden-267":7.5,"shippuden-268":7.4,"shippuden-269":7.7,"shippuden-270":7.8,
    "shippuden-271":5.5,"shippuden-272":7.7,"shippuden-273":7.2,"shippuden-274":7.5,"shippuden-275":8.0,
    "shippuden-276":7.8,"shippuden-277":7.2,"shippuden-278":7.2,"shippuden-279":6.9,"shippuden-280":6.6,
    "shippuden-281":5.0,"shippuden-282":7.7,"shippuden-283":8.1,"shippuden-284":7.1,"shippuden-285":6.6,
    "shippuden-286":6.2,"shippuden-287":6.1,"shippuden-288":6.4,"shippuden-289":6.5,"shippuden-290":6.3,
    "shippuden-291":6.1,"shippuden-292":6.5,"shippuden-293":6.2,"shippuden-294":6.4,"shippuden-295":6.8,
    "shippuden-296":7.6,"shippuden-297":8.4,"shippuden-298":9.0,"shippuden-299":8.8,"shippuden-300":7.9,
    "shippuden-301":8.2,"shippuden-302":7.7,"shippuden-303":6.6,"shippuden-304":6.3,"shippuden-305":6.4,
    "shippuden-306":6.1,"shippuden-307":6.2,"shippuden-308":6.1,"shippuden-309":5.3,"shippuden-310":5.5,
    "shippuden-311":7.3,"shippuden-312":5.4,"shippuden-313":4.6,"shippuden-314":4.9,"shippuden-315":5.4,
    "shippuden-316":5.9,"shippuden-317":6.4,"shippuden-318":6.1,"shippuden-319":6.5,"shippuden-320":6.1,
    "shippuden-321":8.1,"shippuden-322":9.6,"shippuden-323":9.0,"shippuden-324":7.6,"shippuden-325":8.1,
    "shippuden-326":8.2,"shippuden-327":7.2,"shippuden-328":7.8,"shippuden-329":9.3,"shippuden-330":7.6,
    "shippuden-331":6.7,"shippuden-332":8.1,"shippuden-333":8.5,"shippuden-334":8.4,"shippuden-335":7.7,
    "shippuden-336":7.8,"shippuden-337":8.3,"shippuden-338":8.4,"shippuden-339":9.6,"shippuden-340":8.4,
    "shippuden-341":8.1,"shippuden-342":8.8,"shippuden-343":9.3,"shippuden-344":8.8,"shippuden-345":9.6,
    "shippuden-346":8.2,"shippuden-347":7.5,"shippuden-348":8.0,"shippuden-349":7.6,"shippuden-350":7.7,
    "shippuden-351":7.1,"shippuden-352":6.7,"shippuden-353":6.7,"shippuden-354":6.7,"shippuden-355":7.1,
    "shippuden-356":7.1,"shippuden-357":7.6,"shippuden-358":8.1,"shippuden-359":8.0,"shippuden-360":7.5,
    "shippuden-361":7.9,"shippuden-362":8.8,"shippuden-363":9.2,"shippuden-364":9.6,"shippuden-365":9.3,
    "shippuden-366":9.3,"shippuden-367":8.8,"shippuden-368":9.1,"shippuden-369":8.8,"shippuden-370":8.9,
    "shippuden-371":8.6,"shippuden-372":9.4,"shippuden-373":8.8,"shippuden-374":8.6,"shippuden-375":9.6,
    "shippuden-376":4.0,"shippuden-377":3.5,"shippuden-378":8.7,"shippuden-379":8.9,"shippuden-380":8.8,
    "shippuden-381":8.9,"shippuden-382":8.7,"shippuden-383":8.5,"shippuden-384":8.8,"shippuden-385":7.9,
    "shippuden-386":7.8,"shippuden-387":8.3,"shippuden-388":6.1,"shippuden-389":6.1,"shippuden-390":6.4,
    "shippuden-391":8.9,"shippuden-392":8.8,"shippuden-393":9.2,"shippuden-394":6.1,"shippuden-395":5.8,
    "shippuden-396":6.3,"shippuden-397":6.4,"shippuden-398":6.0,"shippuden-399":5.9,"shippuden-400":5.8,
    "shippuden-401":6.5,"shippuden-402":5.4,"shippuden-403":5.5,"shippuden-404":5.4,"shippuden-405":5.6,
    "shippuden-406":5.4,"shippuden-407":5.5,"shippuden-408":5.7,"shippuden-409":5.8,"shippuden-410":5.8,
    "shippuden-411":5.7,"shippuden-412":5.8,"shippuden-413":6.1,"shippuden-414":8.6,"shippuden-415":8.2,
    "shippuden-416":6.8,"shippuden-417":7.9,"shippuden-418":8.3,"shippuden-419":8.7,"shippuden-420":9.2,
    "shippuden-421":9.7,"shippuden-422":6.1,"shippuden-423":6.4,"shippuden-424":9.3,"shippuden-425":9.1,
    "shippuden-426":8.3,"shippuden-427":5.7,"shippuden-428":5.8,"shippuden-429":5.0,"shippuden-430":5.0,
    "shippuden-431":5.9,"shippuden-432":5.3,"shippuden-433":5.3,"shippuden-434":4.7,"shippuden-435":4.8,
    "shippuden-436":4.8,"shippuden-437":4.9,"shippuden-438":5.1,"shippuden-439":5.3,"shippuden-440":5.3,
    "shippuden-441":5.0,"shippuden-442":5.6,"shippuden-443":5.4,"shippuden-444":5.5,"shippuden-445":5.1,
    "shippuden-446":5.2,"shippuden-447":5.1,"shippuden-448":4.9,"shippuden-449":4.6,"shippuden-450":5.6,
    "shippuden-451":7.7,"shippuden-452":7.8,"shippuden-453":7.1,"shippuden-454":7.9,"shippuden-455":9.0,
    "shippuden-456":8.0,"shippuden-457":8.1,"shippuden-458":8.4,"shippuden-459":8.4,"shippuden-460":7.5,
    "shippuden-461":7.7,"shippuden-462":8.2,"shippuden-463":8.3,"shippuden-464":7.5,"shippuden-465":7.3,
    "shippuden-466":7.2,"shippuden-467":7.6,"shippuden-468":8.1,"shippuden-469":8.0,"shippuden-470":8.4,
    "shippuden-471":8.3,"shippuden-472":8.7,"shippuden-473":9.0,"shippuden-474":9.6,"shippuden-475":8.7,
    "shippuden-476":9.5,"shippuden-477":9.5,"shippuden-478":9.6,"shippuden-479":9.2,"shippuden-480":7.2,
    "shippuden-481":6.3,"shippuden-482":6.4,"shippuden-483":6.5,"shippuden-484":7.1,"shippuden-485":7.1,
    "shippuden-486":7.1,"shippuden-487":6.7,"shippuden-488":7.6,"shippuden-489":7.1,"shippuden-490":6.7,
    "shippuden-491":6.7,"shippuden-492":6.7,"shippuden-493":7.1,"shippuden-494":7.0,"shippuden-495":6.5,
    "shippuden-496":7.3,"shippuden-497":7.0,"shippuden-498":6.3,"shippuden-499":7.4,"shippuden-500":9.3,
}

# ─────────────────────────────────────────────────────────────────
# ARC DATA BUILDER
# ─────────────────────────────────────────────────────────────────
def _n(a, b, t):
    return [{"id": f"naruto-{i}", "num": i,
             "title": EP_TITLES_N.get(i, f"Episode {i}"), "type": t}
            for i in range(a, b + 1)]

def _s(a, b, t):
    return [{"id": f"shippuden-{i}", "num": i,
             "title": EP_TITLES_S.get(i, f"Shippuden Episode {i}"), "type": t}
            for i in range(a, b + 1)]

ARCS = [
    # ── NARUTO ORIGINAL ──────────────────────────────────────────
    {"id":"arc-0",    "series":"naruto",    "name":"Land of Waves Arc",
     "eps": _n(1,19,"canon")},
    {"id":"arc-1",    "series":"naruto",    "name":"Chunin Exams Arc",
     "eps": _n(20,25,"canon")+_n(26,26,"filler")+_n(27,67,"canon")},
    {"id":"arc-2",    "series":"naruto",    "name":"Konoha Crush Arc",
     "eps": _n(68,80,"canon")},
    {"id":"arc-3",    "series":"naruto",    "name":"Search for Tsunade Arc",
     "eps": _n(81,96,"canon")+_n(97,97,"filler")+_n(98,100,"canon")},
    {"id":"arc-4",    "series":"naruto",    "name":"Filler — Land of Tea Arc",
     "eps": _n(101,106,"filler")},
    {"id":"arc-5",    "series":"naruto",    "name":"Sasuke Retrieval Arc",
     "eps": _n(107,135,"canon")},
    {"id":"arc-6",    "series":"naruto",    "name":"Filler — Land of Rice Fields Arc",
     "eps": _n(136,140,"filler")+_n(141,142,"canon")},
    {"id":"arc-7",    "series":"naruto",    "name":"Filler — Chunin Exam Retake Arc",
     "eps": _n(143,219,"filler")},
    {"id":"arc-8",    "series":"naruto",    "name":"Epilogue",
     "eps": [{"id":"naruto-220","num":220,"title":"The Top-Secret Mission Begins","type":"canon"}]},

    # ── MOVIES ───────────────────────────────────────────────────
    {"id":"arc-m1",   "series":"movies",    "name":"Naruto Films (Part I)",
     "eps": [
         {"id":"movie-1","num":"Film 1","title":"Ninja Clash in the Land of Snow (2004)","type":"movie"},
         {"id":"movie-2","num":"Film 2","title":"Legend of the Stone of Gelel (2005)","type":"movie"},
         {"id":"movie-3","num":"Film 3","title":"Guardians of the Crescent Moon Kingdom (2006)","type":"movie"},
     ]},
    {"id":"arc-m2",   "series":"movies",    "name":"Naruto Shippuden Films",
     "eps": [
         {"id":"movie-4","num":"Film 4","title":"Shippuden Movie 1 — Shippuden (2007)","type":"movie"},
         {"id":"movie-5","num":"Film 5","title":"Shippuden Movie 2 — Bonds (2008)","type":"movie"},
         {"id":"movie-6","num":"Film 6","title":"Shippuden Movie 3 — Will of Fire (2009)","type":"movie"},
         {"id":"movie-7","num":"Film 7","title":"Shippuden Movie 4 — The Lost Tower (2010)","type":"movie"},
         {"id":"movie-8","num":"Film 8","title":"Shippuden Movie 5 — Blood Prison (2011)","type":"movie"},
         {"id":"movie-9","num":"Film 9","title":"Shippuden Movie 6 — Road to Ninja (2012)","type":"movie"},
     ]},
    {"id":"arc-m3",   "series":"movies",    "name":"The Last & Boruto Films",
     "eps": [
         {"id":"movie-10","num":"Film 10","title":"The Last: Naruto the Movie (2014)","type":"movie"},
         {"id":"movie-11","num":"Film 11","title":"Boruto: Naruto the Movie (2015)","type":"movie"},
     ]},

    # ── SHIPPUDEN ────────────────────────────────────────────────
    {"id":"arc-s1",   "series":"shippuden", "name":"Kazekage Rescue Arc",
     "eps": _s(1,32,"canon")},
    {"id":"arc-s3",   "series":"shippuden", "name":"Tenchi Bridge Reconnaissance Arc",
     "eps": _s(33,53,"canon")},
    {"id":"arc-s2",   "series":"shippuden", "name":"Twelve Guardian Ninja Arc",
     "eps": _s(54,56,"canon")+_s(57,71,"filler")},
    {"id":"arc-s4",   "series":"shippuden", "name":"Akatsuki Suppression Arc",
     "eps": _s(72,90,"canon")},
    {"id":"arc-s5",   "series":"shippuden", "name":"Filler — Three-Tails Arc",
     "eps": _s(91,112,"filler")},
    {"id":"arc-s6",   "series":"shippuden", "name":"Itachi Pursuit / Fated Battle Arc",
     "eps": _s(113,143,"canon")},
    {"id":"arc-s7",   "series":"shippuden", "name":"Filler — Six-Tails Unleashed",
     "eps": _s(144,151,"filler")},
    {"id":"arc-s8",   "series":"shippuden", "name":"Pain's Assault Arc",
     "eps": _s(152,169,"canon")+_s(170,171,"filler")+_s(172,175,"canon")},
    {"id":"arc-s10",  "series":"shippuden", "name":"Filler — Past Arc: The Locus of Konoha",
     "eps": _s(176,196,"filler")},
    {"id":"arc-s9",   "series":"shippuden", "name":"Five Kage Summit Arc",
     "eps": _s(197,222,"canon")},
    {"id":"arc-s12",  "series":"shippuden", "name":"Filler — Paradise Life on a Boat",
     "eps": _s(223,242,"filler")},
    {"id":"arc-s11",  "series":"shippuden", "name":"Fourth Shinobi World War: Countdown",
     "eps": _s(243,256,"canon")},
    {"id":"arc-s13",  "series":"shippuden", "name":"Fourth Shinobi World War: Confrontation",
     "eps": _s(257,260,"filler")+_s(261,270,"canon")+_s(271,271,"filler")+_s(272,278,"canon")+_s(279,281,"filler")+_s(282,283,"canon")+_s(284,289,"filler")},
    {"id":"arc-s14",  "series":"shippuden", "name":"Filler — Power Arc",
     "eps": _s(290,295,"filler")},
    {"id":"arc-s15a", "series":"shippuden", "name":"Fourth Shinobi World War: Attackers from Beyond",
     "eps": _s(296,302,"canon")+_s(303,320,"filler")},
    {"id":"arc-s15b", "series":"shippuden", "name":"Fourth Shinobi World War: Climax (Part 1)",
     "eps": _s(321,346,"canon")+_s(347,348,"filler")},
    {"id":"arc-s15c", "series":"shippuden", "name":"Kakashi's Anbu Arc",
     "eps": _s(349,361,"filler")},
    {"id":"arc-s15d", "series":"shippuden", "name":"Fourth Shinobi World War: Climax (Part 2)",
     "eps": _s(362,375,"canon")+_s(376,377,"filler")},
    {"id":"arc-s15e", "series":"shippuden", "name":"Birth of the Ten-Tails' Jinchuriki (Part 1)",
     "eps": _s(378,387,"canon")+_s(388,390,"filler")+_s(391,393,"canon")},
    {"id":"arc-s15f", "series":"shippuden", "name":"Filler — In Naruto's Footsteps",
     "eps": _s(394,413,"filler")},
    {"id":"arc-s15g", "series":"shippuden", "name":"Birth of the Ten-Tails' Jinchuriki (Part 2)",
     "eps": _s(414,415,"canon")+_s(416,417,"filler")+_s(418,421,"canon")+_s(422,423,"filler")+_s(424,426,"canon")+_s(427,431,"filler")},
    {"id":"arc-s16",  "series":"shippuden", "name":"Filler — Jiraiya Shinobi Handbook",
     "eps": _s(432,450,"filler")},
    {"id":"arc-s17",  "series":"shippuden", "name":"Kaguya Otsutsuki Strikes Arc",
     "eps": _s(451,463,"canon")+_s(464,468,"filler")},
    {"id":"arc-s18",  "series":"shippuden", "name":"Sasuke Shinden / Birth of Naruto",
     "eps": _s(469,479,"canon")},
    {"id":"arc-s19",  "series":"shippuden", "name":"Naruto's Wedding Arc",
     "eps": _s(480,483,"filler")+_s(484,500,"canon")},
]

def arc_badge(arc):
    """Determine display badge type from episode types."""
    types = {ep["type"] for ep in arc["eps"]}
    if types == {"movie"}:
        return "movie"
    if types == {"filler"}:
        return "filler"
    if types == {"canon"} or types == {"canon", "movie"}:
        return "canon"
    return "mixed"

def build_ordered_eps():
    """All episodes in watch order: naruto sorted, shippuden sorted, movies in order."""
    naruto, shippuden, movies = [], [], []
    for arc in ARCS:
        for ep in arc["eps"]:
            if arc["series"] == "naruto":
                naruto.append(ep)
            elif arc["series"] == "shippuden":
                shippuden.append(ep)
            else:
                movies.append(ep)
    naruto.sort(key=lambda e: e["num"])
    shippuden.sort(key=lambda e: e["num"])
    return naruto + shippuden + movies

ALL_EPS = build_ordered_eps()

# ─────────────────────────────────────────────────────────────────
# PROGRESS PERSISTENCE
# ─────────────────────────────────────────────────────────────────
def load_progress():
    try:
        if PROGRESS_FILE.exists():
            return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}

def save_progress(watched: dict):
    try:
        PROGRESS_FILE.write_text(json.dumps(watched, indent=2), encoding="utf-8")
    except Exception:
        pass

# ─────────────────────────────────────────────────────────────────
# STATS
# ─────────────────────────────────────────────────────────────────
def compute_stats(watched):
    def count(eps):
        total = len(eps)
        done = sum(1 for e in eps if watched.get(e["id"]))
        canon_total = sum(1 for e in eps if e["type"] in ("canon", "movie"))
        canon_done  = sum(1 for e in eps if e["type"] in ("canon", "movie") and watched.get(e["id"]))
        filler_total = sum(1 for e in eps if e["type"] == "filler")
        filler_done  = sum(1 for e in eps if e["type"] == "filler" and watched.get(e["id"]))
        return dict(total=total, done=done,
                    canon_total=canon_total, canon_done=canon_done,
                    filler_total=filler_total, filler_done=filler_done)

    naruto_eps   = [e for a in ARCS if a["series"]=="naruto"    for e in a["eps"]]
    ship_eps     = [e for a in ARCS if a["series"]=="shippuden" for e in a["eps"]]
    movie_eps    = [e for a in ARCS if a["series"]=="movies"    for e in a["eps"]]

    return {
        "naruto":    count(naruto_eps),
        "shippuden": count(ship_eps),
        "movies":    count(movie_eps),
        "all":       count(ALL_EPS),
    }

# ─────────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────────────
if "watched" not in st.session_state:
    st.session_state.watched = load_progress()

if "filter" not in st.session_state:
    st.session_state.filter = "All"

# ─────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────
def toggle_ep(ep_id):
    w = st.session_state.watched
    if w.get(ep_id):
        del w[ep_id]
    else:
        w[ep_id] = True
    save_progress(w)

def check_all_arc(arc):
    for ep in arc["eps"]:
        st.session_state.watched[ep["id"]] = True
        key = f"cb_{ep['id']}"
        if key in st.session_state:
            st.session_state[key] = True
    save_progress(st.session_state.watched)

def uncheck_all_arc(arc):
    for ep in arc["eps"]:
        st.session_state.watched.pop(ep["id"], None)
        key = f"cb_{ep['id']}"
        if key in st.session_state:
            st.session_state[key] = False
    save_progress(st.session_state.watched)

def reset_all():
    st.session_state.watched = {}
    for key in list(st.session_state.keys()):
        if key.startswith("cb_"):
            st.session_state[key] = False
    save_progress({})

def pct(done, total):
    return round(done / total * 100) if total else 0

def series_status(p):
    if p == 100:
        return "✅ Complete"
    if p > 0:
        return "▶ In Progress"
    return "○ Not Started"

# ─────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 忍 Shinobi Log")
    st.markdown("*OriLeo's Naruto Watch Tracker*")
    st.divider()

    page = st.radio("Navigate", ["🏠 Home", "📺 Tracker"], label_visibility="collapsed")
    st.divider()

    stats = compute_stats(st.session_state.watched)
    a = stats["all"]
    overall = pct(a["done"], a["total"])
    st.markdown(f"**Overall Progress**")
    st.progress(overall / 100)
    st.caption(f"{a['done']} / {a['total']} episodes — {overall}%")
    st.divider()

    st.markdown("**Save / Restore Progress**")
    progress_json = json.dumps(st.session_state.watched, indent=2)
    st.download_button(
        "⬇ Download progress.json",
        data=progress_json,
        file_name="shinobi_progress.json",
        mime="application/json",
        use_container_width=True,
    )
    uploaded = st.file_uploader("⬆ Upload progress.json", type="json",
                                 label_visibility="collapsed")
    if uploaded is not None:
        try:
            imported = json.load(uploaded)
            st.session_state.watched = imported
            save_progress(imported)
            st.success("Progress restored!")
            st.rerun()
        except Exception as e:
            st.error(f"Invalid file: {e}")

# ─────────────────────────────────────────────────────────────────
# HOME PAGE
# ─────────────────────────────────────────────────────────────────
def render_home():
    st.markdown("# 🍥 Shinobi Log")
    st.markdown("*Track every episode across the Original Series, Shippuden, and the films.*")

    stats = compute_stats(st.session_state.watched)
    a = stats["all"]
    overall = pct(a["done"], a["total"])

    # ── Continue Watching ────────────────────────────────────────
    next_ep = next((e for e in ALL_EPS if not st.session_state.watched.get(e["id"])), None)

    if next_ep is None:
        st.success("🎉 **You completed everything!** Every episode and film checked off. Legendary.")
    else:
        series_label = {"naruto":"Naruto", "shippuden":"Shippuden"}.get(
            next((a["series"] for a in ARCS if any(e["id"]==next_ep["id"] for e in a["eps"])), "movies"),
            "Movies"
        )
        arc_name = next(
            (a["name"] for a in ARCS if any(e["id"]==next_ep["id"] for e in a["eps"])), ""
        )
        ep_label = f"Episode {next_ep['num']}" if isinstance(next_ep["num"], int) else next_ep["num"]
        ep_type = next_ep["type"]
        badge_html = f'<span class="badge-{ep_type}">{ep_type.upper()}</span>'

        with st.container(border=True):
            col_info, col_btn = st.columns([3, 1])
            with col_info:
                st.markdown(f"**▶ Continue Watching**")
                st.markdown(f"*{series_label} · {ep_label}* — {badge_html}", unsafe_allow_html=True)
                st.markdown(f"### {next_ep['title']}")
                st.caption(arc_name)
            with col_btn:
                rating = EP_RATINGS.get(next_ep["id"])
                if rating:
                    st.markdown(f'<div class="star-rating">★ {rating}</div>', unsafe_allow_html=True)
                if st.button("✓ Mark as Watched", type="primary", use_container_width=True):
                    st.session_state.watched[next_ep["id"]] = True
                    save_progress(st.session_state.watched)
                    st.rerun()

    st.divider()

    # ── Stats Row ────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Watched", a["done"])
    c2.metric("Remaining", a["total"] - a["done"])
    c3.metric("Canon Done", a["canon_done"])
    c4.metric("Complete", f"{overall}%")

    st.divider()

    # ── Series Cards ─────────────────────────────────────────────
    st.markdown("### By Series")
    sc1, sc2, sc3 = st.columns(3)

    def series_card(col, title, series_key, color_emoji):
        s = stats[series_key]
        p = pct(s["done"], s["total"])
        with col:
            with st.container(border=True):
                st.markdown(f"**{color_emoji} {title}**")
                st.markdown(f"*{series_status(p)}*")
                st.progress(p / 100)
                st.caption(f"{s['done']} / {s['total']} · {p}%")
                if series_key != "movies":
                    st.caption(f"Canon: {s['canon_done']} / {s['canon_total']}")

    series_card(sc1, "Naruto",    "naruto",    "🟠")
    series_card(sc2, "Shippuden", "shippuden", "🔵")
    series_card(sc3, "Movies",    "movies",    "🟡")

    st.divider()

    # ── Overall Progress ─────────────────────────────────────────
    st.markdown("### Overall Progress")
    oc1, oc2 = st.columns([2, 1])
    with oc1:
        with st.container(border=True):
            st.markdown(f"**{overall}%** complete")
            st.progress(overall / 100)
            canon_pct = a["canon_done"] / a["total"] if a["total"] else 0
            filler_pct = a["filler_done"] / a["total"] if a["total"] else 0
            st.caption(
                f"🟠 Canon & Movies: {a['canon_done']}  ·  "
                f"🟣 Filler: {a['filler_done']}  ·  "
                f"⬜ Unwatched: {a['total'] - a['done']}"
            )
    with oc2:
        with st.container(border=True):
            hours = round(a["done"] * 23 / 60)
            st.metric("Hours Watched", hours)
            st.caption("~23 min per episode")
            st.metric("Filler Done", a["filler_done"])
            st.caption(f"of {a['filler_total']} filler eps")


# ─────────────────────────────────────────────────────────────────
# TRACKER PAGE
# ─────────────────────────────────────────────────────────────────
def render_tracker():
    stats = compute_stats(st.session_state.watched)
    a = stats["all"]
    overall = pct(a["done"], a["total"])

    st.markdown("# 📺 Watch Tracker")
    st.caption("Original Series · Shippuden · Movies — every episode, every arc")

    # Stats bar
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Watched", a["done"])
    c2.metric("Remaining", a["total"] - a["done"])
    c3.metric("Canon Done", a["canon_done"])
    c4.metric("Complete", f"{overall}%")

    st.progress(overall / 100)

    # Controls
    col_filter, col_actions = st.columns([3, 1])
    with col_filter:
        st.session_state.filter = st.radio(
            "Filter",
            ["All", "Canon Only", "Filler Only", "Unwatched"],
            horizontal=True,
            label_visibility="collapsed",
        )
    with col_actions:
        if st.button("🗑 Reset All Progress", type="secondary"):
            reset_all()
            st.rerun()

    st.divider()

    active_filter = st.session_state.filter
    watched = st.session_state.watched

    def should_show(ep):
        if active_filter == "Canon Only":
            return ep["type"] in ("canon", "movie")
        if active_filter == "Filler Only":
            return ep["type"] == "filler"
        if active_filter == "Unwatched":
            return not watched.get(ep["id"])
        return True

    def render_series(series_id, title, series_arcs):
        series_eps = [e for a in series_arcs for e in a["eps"]]
        s = compute_stats(watched)
        sv = s.get(series_id, s["all"])
        done, total = sv["done"], sv["total"]
        p = pct(done, total)

        st.markdown(f"## {title}")
        st.progress(p / 100)
        st.caption(f"{done} / {total} · {p}%")

        for arc in series_arcs:
            visible_eps = [e for e in arc["eps"] if should_show(e)]
            if not visible_eps:
                continue

            arc_done = sum(1 for e in arc["eps"] if watched.get(e["id"]))
            arc_total = len(arc["eps"])
            badge = arc_badge(arc)
            badge_html = f'<span class="badge-{badge}">{badge.upper()}</span>'

            label = (
                f"{arc['name']}  —  {arc_done}/{arc_total}"
            )

            with st.expander(label, expanded=False):
                st.markdown(badge_html, unsafe_allow_html=True)
                bcol1, bcol2 = st.columns(2)
                if bcol1.button("✓ Check All", key=f"ca_{arc['id']}"):
                    check_all_arc(arc)
                    st.rerun()
                if bcol2.button("✗ Uncheck All", key=f"ua_{arc['id']}"):
                    uncheck_all_arc(arc)
                    st.rerun()

                for ep in visible_eps:
                    ep_id = ep["id"]
                    is_watched = bool(watched.get(ep_id))

                    if ep_id not in st.session_state or f"cb_{ep_id}" not in st.session_state:
                        st.session_state[f"cb_{ep_id}"] = is_watched

                    row = st.columns([0.05, 0.08, 0.55, 0.15, 0.12, 0.05])
                    with row[0]:
                        new_val = st.checkbox(
                            "", key=f"cb_{ep_id}",
                            value=is_watched,
                            label_visibility="collapsed",
                        )
                        if new_val != is_watched:
                            if new_val:
                                st.session_state.watched[ep_id] = True
                            else:
                                st.session_state.watched.pop(ep_id, None)
                            save_progress(st.session_state.watched)
                            st.rerun()

                    with row[1]:
                        num_str = str(ep["num"])
                        st.caption(num_str)

                    with row[2]:
                        title_cls = "ep-title-watched" if is_watched else ""
                        st.markdown(
                            f'<span class="{title_cls}">{ep["title"]}</span>',
                            unsafe_allow_html=True,
                        )

                    with row[3]:
                        t = ep["type"]
                        st.markdown(
                            f'<span class="badge-{t}">{t.upper()}</span>',
                            unsafe_allow_html=True,
                        )

                    with row[4]:
                        r = EP_RATINGS.get(ep_id)
                        if r:
                            st.markdown(
                                f'<span class="star-rating">★ {r}</span>',
                                unsafe_allow_html=True,
                            )

        st.divider()

    naruto_arcs    = [a for a in ARCS if a["series"] == "naruto"]
    shippuden_arcs = [a for a in ARCS if a["series"] == "shippuden"]
    movie_arcs     = [a for a in ARCS if a["series"] == "movies"]

    render_series("naruto",    "🟠 Naruto — Original Series",       naruto_arcs)
    render_series("movies",    "🟡 Movies",                          movie_arcs)
    render_series("shippuden", "🔵 Naruto Shippuden",               shippuden_arcs)

# ─────────────────────────────────────────────────────────────────
# MAIN ROUTER
# ─────────────────────────────────────────────────────────────────
if page == "🏠 Home":
    render_home()
else:
    render_tracker()
