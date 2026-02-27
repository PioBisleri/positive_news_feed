"""
Seed script — run directly: python seed.py
Uses synchronous psycopg (v3) to keep the seed logic simple.
"""
import os
import random
from datetime import datetime, timedelta, timezone

import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:password@localhost:5432/positivenews"
)

CATEGORIES = [
    {"name": "Science", "emoji": "🔬", "color": "bg-blue-100 text-blue-800"},
    {"name": "Environment", "emoji": "🌿", "color": "bg-green-100 text-green-800"},
    {"name": "Community", "emoji": "🤝", "color": "bg-purple-100 text-purple-800"},
    {"name": "Health", "emoji": "💪", "color": "bg-red-100 text-red-800"},
    {"name": "Animals", "emoji": "🐾", "color": "bg-yellow-100 text-yellow-800"},
    {"name": "Technology", "emoji": "💡", "color": "bg-indigo-100 text-indigo-800"},
    {"name": "Arts & Culture", "emoji": "🎨", "color": "bg-pink-100 text-pink-800"},
]

ARTICLES = [
    # Science
    {
        "title": "Scientists Discover Gene That Could Halt Alzheimer's Progression",
        "summary": "Researchers at the University of Cambridge have identified a gene variant that dramatically slows the buildup of amyloid plaques in the brain, offering new hope for millions of Alzheimer's patients worldwide.",
        "content": """A groundbreaking discovery from the University of Cambridge is giving millions of families new hope in the fight against Alzheimer's disease. Scientists have identified a rare gene variant, dubbed ARCH-7, that appears to dramatically slow the formation of amyloid plaques — the protein clusters long associated with cognitive decline.

The team, led by Professor Sarah Hendricks, spent seven years tracking 4,200 participants across Europe and North America. Those carrying the ARCH-7 variant showed 68% less plaque accumulation compared to a control group at the same age, and many remained cognitively sharp well into their late eighties. "What's extraordinary is that this gene isn't just slowing Alzheimer's — it seems to be actively clearing the brain's debris," Hendricks said.

Pharmaceutical companies are already in conversation with the research team about developing a synthetic version of the gene's protective protein. Early lab trials on mouse models showed a 40% improvement in memory retention after just six weeks of treatment. Human trials are expected to begin within two years.

Advocacy groups praised the announcement as a watershed moment. "For too long, families have watched helplessly. This research changes the conversation from managing decline to actively preventing it," said James Cole, CEO of Alzheimer's International Hope Foundation. Funding for the next phase of research has already been secured from a coalition of public health bodies and private donors.""",
        "image_url": "https://picsum.photos/seed/alzheimer/800/500",
        "source": "Cambridge Science Review",
        "author": "Dr. Eleanor Marsh",
        "category": "Science",
        "is_featured": True,
        "days_ago": 1,
    },
    {
        "title": "CRISPR Therapy Cures Sickle Cell Disease in 94% of Trial Patients",
        "summary": "A landmark gene-editing trial has freed dozens of sickle cell patients from a lifetime of pain crises, marking one of the most significant medical breakthroughs of the decade.",
        "content": """In what experts are calling a defining moment in modern medicine, a new CRISPR-based gene therapy has eliminated sickle cell disease symptoms in 94% of clinical trial participants — with results lasting over three years and counting.

The therapy, developed by BioGene Therapeutics, works by editing the patient's own stem cells to produce healthy hemoglobin rather than the misshapen variant responsible for sickle cell's characteristic blood flow blockages. Participants described the transformation as life-changing — many had experienced debilitating pain crises multiple times a month before treatment.

"I haven't had a single crisis in eighteen months," said Marcus Williams, 28, one of the trial's earliest participants. "I used to plan my life around hospital visits. Now I'm planning a hiking trip." His story is echoed by dozens of others in the cohort, who report dramatic improvements in energy, sleep, and overall quality of life.

The FDA has granted the therapy Breakthrough Therapy designation, fast-tracking its path to wider approval. Advocates are now pushing for insurance coverage reform to ensure equitable access, particularly for communities in sub-Saharan Africa and South Asia where sickle cell disease disproportionately affects populations.""",
        "image_url": "https://picsum.photos/seed/crispr/800/500",
        "source": "Global Health Today",
        "author": "Dr. Priya Nair",
        "category": "Science",
        "is_featured": False,
        "days_ago": 3,
    },
    # Environment
    {
        "title": "Great Barrier Reef Records Highest Coral Cover in 36 Years",
        "summary": "The Australian Institute of Marine Science reports that coral cover on the northern Great Barrier Reef has reached 36% — its highest level since monitoring began — thanks to coordinated conservation efforts and reduced bleaching events.",
        "content": """Australia's Great Barrier Reef is bouncing back, and scientists are cautiously celebrating what appears to be the reef's strongest recovery in nearly four decades. New data from the Australian Institute of Marine Science shows coral cover on the northern reef system has climbed to 36%, the highest recorded figure since systematic monitoring began in 1986.

The recovery has been credited to a combination of factors: reduced agricultural runoff following tighter land-use regulations in Queensland, lower-than-average sea temperatures during two consecutive La Niña events, and the success of crown-of-thorns starfish control programs that have ramped up in recent years. "We're seeing juvenile coral colonies in areas that were almost bare four years ago," said Dr. Alicia Tobin, a marine biologist with AIMS. "These juveniles represent the reef's future."

Community-led coral restoration projects have also played a measurable role. Over 200 trained volunteers have spent weekends planting heat-resistant coral strains cultivated in floating nurseries off Cairns and Townsville. Several Indigenous ranger groups have expanded their sea country stewardship programs, incorporating traditional ecological knowledge into modern conservation practice.

Scientists caution that climate change remains the reef's single greatest threat and that sustained political commitment to emissions reduction is critical to preserving these gains. However, for the millions of divers, researchers, and reef-dependent communities who feared the worst just a few years ago, today's news feels like a genuine turning point.""",
        "image_url": "https://picsum.photos/seed/reef/800/500",
        "source": "Australian Marine Science Journal",
        "author": "Lena Whitmore",
        "category": "Environment",
        "is_featured": True,
        "days_ago": 2,
    },
    {
        "title": "Costa Rica Runs on 100% Renewable Energy for the 300th Consecutive Day",
        "summary": "The Central American nation continues to shatter clean-energy records, demonstrating that a fossil-fuel-free grid is not just possible — it's thriving.",
        "content": """Costa Rica has reached a remarkable milestone: 300 consecutive days powered entirely by renewable energy. The country's national grid, fed by a mix of hydroelectric, geothermal, wind, and solar sources, has not burned a single drop of fossil fuel since last February — and authorities expect the streak to continue well into next year.

The achievement is the result of decades of deliberate infrastructure investment. Costa Rica's state utility, ICE, began pivoting aggressively toward renewables in the 1990s, and today over 80% of the country's power comes from hydroelectric dams fed by its abundant tropical rainfall. Geothermal plants tapping volcanic activity in the Central Cordillera provide a stable baseload, while a rapidly expanding solar sector adds daytime flexibility.

"We took the long view, and it paid off," said Energy Minister Claudia Solano. "Our electricity bills are among the lowest in the region, our air is cleaner, and we've insulated ourselves from global oil price shocks." The country's low energy cost has also attracted clean-tech manufacturers looking for a green supply chain story for their products.

Neighboring nations are paying close attention. Panama and Honduras have sent delegations to study the Costa Rican model, and the Inter-American Development Bank recently announced a $500 million fund to help five Central American countries replicate Costa Rica's grid architecture. Conservationists note that the renewable transition has also helped protect the country's famous biodiversity by reducing the pressure to drill in protected forest areas.""",
        "image_url": "https://picsum.photos/seed/costarica/800/500",
        "source": "Clean Energy Monitor",
        "author": "Sofia Reyes",
        "category": "Environment",
        "is_featured": False,
        "days_ago": 4,
    },
    # Community
    {
        "title": "Detroit Neighborhood Transforms Vacant Lots Into Thriving Urban Farms",
        "summary": "A grassroots initiative in Detroit has converted over 200 vacant lots into productive urban gardens, providing fresh produce to food deserts while rebuilding community bonds.",
        "content": """What was once a patchwork of overgrown, abandoned lots in Detroit's East Side is now a vibrant network of urban farms producing more than 80,000 pounds of fresh vegetables annually. The Green Revive Detroit project, launched by local resident Tanya Brooks in 2019 with just a borrowed tractor and twelve volunteers, has grown into one of the most ambitious urban agriculture programs in the United States.

The initiative now employs 47 full-time staff — most from the surrounding neighborhood — and engages over 600 volunteers each growing season. Partnering with Wayne County, the project converted 217 city-owned vacant parcels into raised-bed gardens, hoop houses, and beehive apiaries. Produce is distributed through a pay-what-you-can farmstand model, ensuring that access isn't gatekept by income.

"People said vacant lots were eyesores and sources of crime," said Brooks. "We said they were opportunities. Now the same blocks that used to cause worry are where kids are learning about soil biology and grandmothers are swapping recipes for the collard greens they picked that morning." Crime statistics in the project's core ZIP codes have dropped 22% since the initiative began, a correlation local officials acknowledge even if they're careful to attribute it to multiple factors.

The model is now being replicated. Cities including Cleveland, Baltimore, and Gary, Indiana, have sent planners to Detroit to study Green Revive's land-acquisition partnerships, volunteer management systems, and soil remediation protocols. A national nonprofit arm is being established to provide seed funding and technical support to cities ready to follow Detroit's lead.""",
        "image_url": "https://picsum.photos/seed/detroit-farm/800/500",
        "source": "Cityscapes Magazine",
        "author": "Jahmal Porter",
        "category": "Community",
        "is_featured": False,
        "days_ago": 5,
    },
    {
        "title": "Scottish Town Becomes First in Europe to Achieve Full Housing Security",
        "summary": "Glenrothes has reached a remarkable milestone: zero families in temporary accommodation, achieved through a decade-long community housing partnership that is now a model for the continent.",
        "content": """The Scottish town of Glenrothes has become the first municipality in Europe to fully eliminate family homelessness, housing every family with children in stable, permanent accommodation. Local officials announced the milestone at a community gathering attended by over 1,000 residents who had contributed to the decade-long effort.

The achievement followed a 2014 pledge by the Fife Council to treat housing as a fundamental right rather than a social service. Working with housing associations, NHS Scotland, and a network of faith communities, the council built 1,400 new affordable homes, converted redundant commercial properties into mixed-use residential buildings, and created a rapid-rehousing pathway that moves families from emergency shelter to permanent housing within an average of 18 days.

Equally important was the wraparound support model. Every newly housed family is assigned a "housing coach" — a trained community worker who helps navigate everything from benefits applications to school enrollment to mental health support. Churn rates (families returning to homelessness) have remained below 4% over the past three years, far below national averages.

Housing Minister Beverley Duncan called Glenrothes "proof that homelessness is always a policy choice, never an inevitability." The Scottish Government has now committed to replicating the model across six more councils by 2027, and delegations from Germany, France, and Ireland have visited to study the program's architecture.""",
        "image_url": "https://picsum.photos/seed/scotland-housing/800/500",
        "source": "The Scotsman",
        "author": "Fiona Campbell",
        "category": "Community",
        "is_featured": False,
        "days_ago": 6,
    },
    # Health
    {
        "title": "New Vaccine Cuts Malaria Deaths in Children by 75% in African Trial",
        "summary": "The R21/Matrix-M malaria vaccine has demonstrated unprecedented efficacy in a large-scale trial across five African nations, potentially saving hundreds of thousands of young lives each year.",
        "content": """Results from the largest malaria vaccine trial ever conducted in Africa have stunned the global health community: the R21/Matrix-M vaccine reduced severe malaria cases in children under five by 75%, a figure that far exceeds the thresholds scientists had hoped for and which, if deployed at scale, could prevent more than 400,000 child deaths annually.

The trial, conducted across Burkina Faso, Kenya, Mali, Tanzania, and Uganda, enrolled over 28,000 children and tracked outcomes over a four-year period. Efficacy remained high even in high-transmission regions where previous vaccines had struggled. "This is the number we've been chasing for fifty years," said Dr. Kwame Asante of the Volta Medical Research Institute, one of the trial's lead investigators. "It changes everything about what's possible."

The vaccine's success stems partly from its partnership with the Matrix-M adjuvant, a compound that dramatically amplifies the immune response, allowing a smaller antigen dose to generate robust protection. The manufacturing process has been designed for scalability: the Serum Institute of India has committed to producing 100 million doses annually at a cost of approximately $3.50 per dose.

GAVI, the Vaccine Alliance, has already announced pre-purchase commitments for 18 African nations. The WHO's Malaria Policy Advisory Group convened an emergency meeting to accelerate recommendation timelines. "Roll-out cannot come soon enough," said Dr. Asante. "Every month of delay represents tens of thousands of children we could have saved."
""",
        "image_url": "https://picsum.photos/seed/malaria-vaccine/800/500",
        "source": "The Lancet Global Health",
        "author": "Dr. Amara Diallo",
        "category": "Health",
        "is_featured": False,
        "days_ago": 2,
    },
    {
        "title": "Mediterranean Diet Shown to Reverse Type 2 Diabetes in 50% of Participants",
        "summary": "A landmark longitudinal study finds that strict adherence to a Mediterranean diet, without calorie restriction, led to full diabetes remission in half of all participants over two years.",
        "content": """A comprehensive two-year study published in the British Medical Journal has found that a Mediterranean-style dietary pattern can reverse Type 2 diabetes in approximately 50% of participants — without any medication changes or calorie counting. The finding challenges longstanding assumptions about the disease's permanence and opens new non-pharmaceutical pathways for the millions living with the condition.

The study followed 1,880 recently diagnosed Type 2 diabetics across Italy, Spain, and Greece. Half were given intensive guidance to adopt a traditional Mediterranean diet rich in olive oil, legumes, whole grains, fish, and vegetables, while reducing red meat and refined carbohydrates. The other half received standard dietary advice. After 24 months, 52% of the Mediterranean group had achieved full glycemic remission — defined as normal blood sugar without diabetes medication — compared to just 9% in the control group.

Researchers attribute the results to the diet's effect on gut microbiome diversity, insulin sensitivity, and systemic inflammation, all of which are implicated in the development of Type 2 diabetes. Notably, weight loss did not appear to be the primary driver: even participants who lost minimal weight showed significant metabolic improvements if they maintained dietary compliance.

"This should change how we counsel newly diagnosed patients," said Professor Lucia Romano of the University of Naples, the study's senior author. "Diet first — aggressive, structured, supported diet — not just as an adjunct to medication but as a potential cure in its own right." Advocacy groups are already calling for Mediterranean dietary counseling to be added to national diabetes management guidelines.""",
        "image_url": "https://picsum.photos/seed/mediterranean/800/500",
        "source": "British Medical Journal",
        "author": "Prof. Lucia Romano",
        "category": "Health",
        "is_featured": False,
        "days_ago": 7,
    },
    # Animals
    {
        "title": "Humpback Whale Population Rebounds to Pre-Whaling Numbers in South Atlantic",
        "summary": "After near-extinction in the 20th century, humpback whale populations in the South Atlantic have fully recovered to pre-industrial levels, a conservation triumph decades in the making.",
        "content": """In one of the most remarkable wildlife recoveries in recorded history, humpback whale populations in the South Atlantic Ocean have returned to their pre-whaling abundance for the first time since commercial hunting devastated their numbers in the early 20th century. Researchers from the International Whaling Commission confirmed the milestone following a decade-long population survey.

At their lowest point in the 1950s, South Atlantic humpback populations had plummeted to fewer than 450 individuals — a fraction of the estimated 27,000 that swam these waters before industrial whaling commenced. The International Whaling Commission's 1986 moratorium on commercial whaling provided the critical breathing room, but recovery was slow and uncertain for decades. Today, the monitored population stands at approximately 25,000, and natural growth momentum suggests numbers will stabilize near historical baselines within a generation.

"This is what conservation success looks like across a generational timescale," said Dr. Vanessa Cruz of the Brazilian Marine Research Institute. "The people who fought for the moratorium in the 1980s didn't live to see today, but their work made this moment possible." Brazil's federal protected ocean zones, which restrict shipping noise and fishing gear in key breeding corridors, played a concrete role in sustaining the recovery.

Scientists note that whale populations serve as an indicator of overall ocean health, as humpbacks occupy a central role in the marine food web. Their thriving numbers bode well for the broader ecosystems of the South Atlantic, including the anchovy and krill populations that feed everything from penguins to albatrosses.""",
        "image_url": "https://picsum.photos/seed/humpback/800/500",
        "source": "Marine Conservation Science",
        "author": "Dr. Vanessa Cruz",
        "category": "Animals",
        "is_featured": False,
        "days_ago": 8,
    },
    {
        "title": "Californian Sea Otters Return to Kelp Forests After 150-Year Absence",
        "summary": "Reintroduced sea otters are rapidly restoring California's kelp forest ecosystems by controlling urchin populations, reversing decades of ecological decline along the Pacific coast.",
        "content": """Sea otters, once hunted to near-extinction along California's coast, are engineering a remarkable ecological revival. Following a carefully managed reintroduction program in coordination with the U.S. Fish and Wildlife Service, otter populations have expanded along 300 miles of California coastline, and the results for the region's iconic kelp forests have been dramatic.

The mechanism is elegant: otters are voracious predators of sea urchins, which in uncontrolled numbers devour kelp at the holdfasts, creating so-called "urchin barrens" — stretches of seabed entirely stripped of their towering kelp canopy. With otters back in the ecosystem, urchin populations are being held in check, and kelp is regrowing at a rate biologists describe as "accelerated beyond our most optimistic projections."

Drone imagery gathered over three consecutive growing seasons shows kelp canopy coverage in otter-occupied zones increasing by an average of 180%. Accompanying this recovery is a cascade of returning biodiversity: lingcod, rockfish, and leopard sharks are following the kelp back, and certain seabird colonies that depend on the fish-rich kelp understory have doubled in size. "These otters are doing conservation work that would cost millions of dollars in engineered solutions," said Dr. Rachel Ng of the Monterey Bay Aquarium Research Institute.

Fishing communities, initially skeptical of the reintroduction, are reporting improved nearshore fish catches — exactly the kind of ecosystem-service dividend that marine biologists predicted but sometimes struggle to demonstrate with real-world data.""",
        "image_url": "https://picsum.photos/seed/seaotter/800/500",
        "source": "Pacific Ecology Review",
        "author": "Dr. Rachel Ng",
        "category": "Animals",
        "is_featured": False,
        "days_ago": 9,
    },
    # Technology
    {
        "title": "Solar Panels Reach 47% Efficiency in Lab Breakthrough",
        "summary": "Engineers at MIT have shattered previous solar cell efficiency records, potentially unlocking a new era of compact, affordable solar energy at a fraction of current costs.",
        "content": """A research team at MIT's Energy Initiative has achieved a photovoltaic efficiency of 47.1% in laboratory conditions — a figure that more than doubles the real-world performance of most commercially available solar panels and shatters the previous certified record of 39.2%. The achievement, published in Nature Energy, is being hailed as a potential turning point for the economics of solar power.

The breakthrough hinges on a novel "tandem" cell architecture that stacks four ultra-thin photovoltaic layers, each tuned to capture a different portion of the solar spectrum. Where conventional silicon panels capture roughly one-fifth of available sunlight, the MIT cell converts nearly half — by capturing wavelengths from ultraviolet through to near-infrared that single-junction cells leave untapped.

Cost has historically been the barrier to multi-junction solar adoption: the technology has existed in spacecraft since the 1990s, but manufacturing complexity made it economically viable only for high-value aerospace applications. The MIT team addressed this by developing a continuous roll-to-roll manufacturing process using abundant, inexpensive perovskite compounds rather than the rare indium and gallium used in aerospace cells.

"If we can scale this to 40% efficiency at commercial costs — even if we fall back from the lab peak — we are looking at solar becoming cheaper than any other energy source in human history," said the project's lead researcher, Professor Ananya Krishnamurthy. The Department of Energy has announced a $480 million grant to support the team's transition from lab prototype to manufacturable product.""",
        "image_url": "https://picsum.photos/seed/solar-panel/800/500",
        "source": "Nature Energy",
        "author": "Prof. Ananya Krishnamurthy",
        "category": "Technology",
        "is_featured": False,
        "days_ago": 3,
    },
    {
        "title": "AI System Deciphers 3,000-Year-Old Tablets, Unlocking Ancient History",
        "summary": "A machine learning model trained on cuneiform script has translated thousands of previously unreadable Babylonian tablets, revealing trade networks, poetry, and medical knowledge lost for millennia.",
        "content": """Historians, archaeologists, and language scholars are celebrating an extraordinary leap forward in the study of the ancient world: an AI system developed by a collaboration between Oxford University and Google DeepMind has successfully translated over 4,000 previously indecipherable Babylonian clay tablets using a sophisticated cuneiform recognition model.

The tablets, many dating between 1000 and 500 BCE, had resisted translation for decades due to damage, unusual scribal dialects, and sheer volume — traditional decipherment of a single complex tablet can take a skilled scholar weeks. The AI model, trained on a digitized corpus of 80,000 already-translated tablets, processed the backlog in a matter of days, producing translations that independent cuneiform experts evaluated as accurate to a high degree of confidence.

Among the discoveries: a previously unknown astronomical text from the Neo-Babylonian period that refines our understanding of ancient planetary observation, a collection of personal letters from a merchant family documenting trade routes between Babylon and Lydia, and several medical treatises describing herbal remedies for conditions including what appear to be depression and chronic joint pain. "This AI didn't just speed up translation — it made translation possible for texts we'd essentially given up on," said Professor Hugh Winterbourne of Oxford's Faculty of Oriental Studies.

The team has made the model open-source and is now partnering with museums in Iraq, Turkey, and Germany that hold tens of thousands of unstudied tablets. The hope is that this approach will, within a decade, substantially complete the translation of the entire known cuneiform archive — one of the most ambitious acts of historical recovery ever undertaken.""",
        "image_url": "https://picsum.photos/seed/cuneiform/800/500",
        "source": "Oxford Historical Review",
        "author": "Prof. Hugh Winterbourne",
        "category": "Technology",
        "is_featured": False,
        "days_ago": 10,
    },
    # Arts & Culture
    {
        "title": "Indigenous Artists Gain Global Recognition at Venice Biennale",
        "summary": "This year's Venice Biennale opened its main exhibition to Indigenous artists from five continents, drawing record attendance and sparking a long-overdue global conversation about representation in fine art.",
        "content": """The 2025 Venice Biennale has opened its central pavilion — one of the most prestigious platforms in the global art world — to a historically unprecedented cohort: 60% of the works in the main exhibition were created by Indigenous artists from Australia, Canada, Brazil, Kenya, and the Pacific Islands. The decision, made by the Biennale's newly appointed curatorial team, has generated enormous critical acclaim and the highest opening-week attendance in the event's 130-year history.

The works on display are as formally diverse as the cultures they represent, ranging from monumental fiber installations by Māori weavers referencing whakapapa (genealogy) to hyper-detailed digital paintings by Anishinaabe artists fusing traditional Woodland imagery with fractured internet iconography. Brazilian Yanomami artist Davi Kopenawa showed a series of shamanic cosmological maps rendered in fluorescent pigments that stopped viewers in their tracks. Critics have called it the most emotionally and intellectually resonant Biennale in a generation.

"The conversation in contemporary art has been too narrow for too long," said curatorial director Isabelle Mwangi. "What happens when you decenter the Western art historical narrative? You get this — you get urgency, spiritual depth, and an entirely different relationship to land, time, and meaning."

Several artists sold major works to leading institutional collections during the opening preview. The Tate Modern, the Guggenheim Bilbao, and the National Gallery of Australia all announced acquisitions. The Biennale is generating broader pressure among gallerists and auction houses to re-examine their own representation gaps, with a coalition of 40 major galleries signing a pledge to increase Indigenous artist representation to at least 25% of exhibitions by 2027.""",
        "image_url": "https://picsum.photos/seed/venice-biennale/800/500",
        "source": "Artforum International",
        "author": "Chiara Lombardi",
        "category": "Arts & Culture",
        "is_featured": False,
        "days_ago": 4,
    },
    {
        "title": "Community Theatre Program Reduces Teen Loneliness by 60% in Pilot Study",
        "summary": "A university-partnered drama program targeting isolated teenagers has shown remarkable results, with participants reporting dramatically reduced loneliness and improved mental health outcomes.",
        "content": """A university-community partnership pilot program offering free theatre training to socially isolated teenagers has produced striking mental health results in its first full-year evaluation: participants reported a 60% reduction in loneliness scores and significant improvements in self-reported anxiety and depression over the 12-month study period.

The program, called Stage Presence, was launched in Leeds, UK, in partnership with the University of Leeds's School of Psychology and four local secondary schools. It recruited 180 teenagers aged 13-17 who had been identified by school counselors as experiencing significant social isolation — a cohort that had grown substantially in the years following the pandemic. Participants attended weekly ensemble theatre workshops, worked toward two public performances per year, and were paired with older mentors from the city's professional theatre community.

Psychologists analyzing the results point to several active ingredients: the structured creative collaboration required participants to practice social attunement skills; the public performance element built incremental tolerance for vulnerability; and the long-term group commitment created a sense of genuine belonging that many participants had never previously experienced. "Theatre uniquely combines emotional risk-taking with physical community," said Dr. Priya Gupta of the University of Leeds. "It's social rehabilitation disguised as art."

The UK Arts Council has awarded Stage Presence a three-year expansion grant to scale the program to 15 cities. Several NHS mental health trusts are consulting with the team about integrating a version of the program into clinical care pathways for adolescents on long waiting lists for counseling services.""",
        "image_url": "https://picsum.photos/seed/theatre/800/500",
        "source": "Journal of Adolescent Psychology",
        "author": "Dr. Priya Gupta",
        "category": "Arts & Culture",
        "is_featured": False,
        "days_ago": 6,
    },
    # Extra articles
    {
        "title": "World's First Plastic-Free Supermarket Chain Expands to 50 Countries",
        "summary": "Loop Market, which pioneered zero-packaging grocery shopping, has signed agreements to expand its reusable-container model across 50 nations, eliminating an estimated 2 billion pieces of single-use plastic annually.",
        "content": """Loop Market, the supermarket concept that replaced all single-use packaging with reusable, deposit-based containers, has announced an expansion into 50 new countries following the resounding success of its flagship stores in the Netherlands, Japan, and Canada. The move is expected to eliminate an estimated 2 billion pieces of plastic packaging from the waste stream annually.

The model is deceptively simple: shoppers pay a refundable deposit on the container for every product they purchase. When they return the container at any Loop location, it is industrially sanitized, refilled by manufacturers, and returned to shelves. The system has achieved a 94% container-return rate in its existing markets — orders of magnitude better than conventional recycling, which typically captures 30-40% of materials even in well-functioning systems.

Major consumer goods companies including Unilever, Procter & Gamble, and Nestlé have signed on as Loop partners, reformulating their products and redesigning packaging specifically for the Loop ecosystem. "We've been waiting for a viable alternative to the throwaway model," said Nestlé's Head of Sustainable Packaging, Petra Klein. "This is it. The unit economics work, and consumers love it."

Governments in the European Union and South Korea have agreed to provide startup grants and zoning support for Loop's expansion, viewing the model as a key component of their extended producer responsibility frameworks. Environmentalists, who have long argued that consumer education campaigns cannot solve the plastic crisis without structural change to how products are sold, are celebrating the move as exactly the kind of systemic intervention they have been advocating for.""",
        "image_url": "https://picsum.photos/seed/plastic-free/800/500",
        "source": "Sustainable Business Weekly",
        "author": "Marta Heikkinen",
        "category": "Environment",
        "is_featured": False,
        "days_ago": 11,
    },
    {
        "title": "Paralyzed Patients Walk Again Thanks to Brain-Spine Interface Implant",
        "summary": "A Swiss-led research team has enabled three patients with complete spinal cord injuries to walk naturally using a wireless brain-computer interface that bypasses the damaged spinal cord in real time.",
        "content": """Three men who had been completely paralyzed below the waist for years have regained the ability to stand, walk, and even climb stairs, following implantation of a novel brain-spine interface developed by researchers at EPFL in Lausanne, Switzerland. The results, published in Nature, represent the most significant advance in spinal cord injury rehabilitation in the field's history.

The system uses electrodes implanted on the surface of the motor cortex to read the patient's movement intentions in real time. A machine-learning algorithm interprets those signals and transmits them wirelessly to a second implant positioned on the lower spinal cord, where tiny pulses of electricity activate the precise motor neurons needed to produce coordinated movement. The whole process happens in under 300 milliseconds — fast enough to feel natural rather than robotic.

What surprised researchers most was what happened over time: even after the device was switched off, all three patients showed measurable spontaneous recovery of some voluntary motor function. Scientists believe the interface may be stimulating neuroplasticity — encouraging the brain and spinal cord to forge new neural pathways around the injury site. "The stimulation isn't just compensating for the injury — it seems to be partially healing it," said Professor Grégoire Courtine, the project's principal investigator.

Clinical trials are now being expanded to 50 patients across Europe and North America. The team is also working on a non-surgical version using high-density surface electrodes, which could eventually make the technology accessible to patients who are not candidates for brain surgery.""",
        "image_url": "https://picsum.photos/seed/brain-spine/800/500",
        "source": "Nature",
        "author": "Prof. Grégoire Courtine",
        "category": "Health",
        "is_featured": False,
        "days_ago": 12,
    },
]

REACTION_TYPES = ["inspiring", "heartwarming", "amazing", "hopeful"]


def run_seed():
    conn = psycopg.connect(DATABASE_URL)
    cur = conn.cursor()

    # Create tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            emoji VARCHAR(10),
            color VARCHAR(50)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id SERIAL PRIMARY KEY,
            title VARCHAR(500) NOT NULL,
            summary TEXT NOT NULL,
            content TEXT,
            image_url VARCHAR(1000),
            source VARCHAR(200),
            author VARCHAR(200),
            published_at TIMESTAMPTZ DEFAULT NOW(),
            category_id INTEGER REFERENCES categories(id),
            is_featured BOOLEAN DEFAULT FALSE,
            is_saved BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reactions (
            id SERIAL PRIMARY KEY,
            article_id INTEGER REFERENCES articles(id) ON DELETE CASCADE,
            reaction_type VARCHAR(50) NOT NULL,
            count INTEGER DEFAULT 0
        )
    """)
    conn.commit()

    # Seed categories
    category_ids = {}
    for cat in CATEGORIES:
        cur.execute(
            """
            INSERT INTO categories (name, emoji, color)
            VALUES (%s, %s, %s)
            ON CONFLICT (name) DO UPDATE SET emoji=EXCLUDED.emoji, color=EXCLUDED.color
            RETURNING id
            """,
            (cat["name"], cat["emoji"], cat["color"]),
        )
        row = cur.fetchone()
        category_ids[cat["name"]] = row[0]
    conn.commit()
    print(f"✅ Seeded {len(CATEGORIES)} categories")

    # Remove existing articles + reactions to allow re-seeding
    cur.execute("DELETE FROM reactions")
    cur.execute("DELETE FROM articles")
    conn.commit()

    # Seed articles
    for art in ARTICLES:
        pub_date = datetime.now(timezone.utc) - timedelta(days=art["days_ago"])
        cat_id = category_ids.get(art["category"])
        cur.execute(
            """
            INSERT INTO articles
                (title, summary, content, image_url, source, author,
                 published_at, category_id, is_featured, is_saved)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING id
            """,
            (
                art["title"],
                art["summary"],
                art["content"],
                art["image_url"],
                art["source"],
                art["author"],
                pub_date,
                cat_id,
                art.get("is_featured", False),
                False,
            ),
        )
        article_id = cur.fetchone()[0]

        # Seed reactions for this article
        for rtype in REACTION_TYPES:
            count = random.randint(10, 500)
            cur.execute(
                "INSERT INTO reactions (article_id, reaction_type, count) VALUES (%s,%s,%s)",
                (article_id, rtype, count),
            )

    conn.commit()
    print(f"✅ Seeded {len(ARTICLES)} articles with reactions")

    cur.close()
    conn.close()
    print("🌟 Database seeding complete!")


if __name__ == "__main__":
    run_seed()
