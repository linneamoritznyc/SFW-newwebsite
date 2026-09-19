/* Every post on page 1 of https://new.soilfoodweb.com/news/, read off the
 * news index on 19 Sep 2026. Titles, categories and dates are verbatim.
 *
 * Two things are NOT verbatim and are marked TODO below:
 *   - author. Only the ciliates post shows its byline in the header we have
 *     seen. The rest are blank rather than guessed.
 *   - image. Every photograph here is a stand-in from this repository. The
 *     real post images have not been downloaded yet.
 *
 * theme: "legacy" puts the panel in Legacy Purple, which css/site.css
 * reserves for Dr. Elaine content. Three posts here are about her.
 */
module.exports = [
  {
    slug: 'ciliates-microscope-watermelon',
    date: '2026-05-01',
    category: 'Microscopy',
    title: 'How A Rare Microscope Sighting Helps Deduce The Problem With Unhealthy Soil: Ciliates, Cysts, and the Clues Hiding in a Struggling Watermelon Crop',
    author: 'Wes Sander',
    image: '../img/w/sfw-amoeba-still-wide.jpg',
    focus: '50% 50%'
  },
  {
    slug: 'permaculture-design-certificate',
    date: '2026-04-13',
    category: 'Blog',
    title: 'The Soil Food Web School Launches Its First-Ever Permaculture Design Certificate Course — A Milestone Moment for Regenerative Education',
    author: '',
    image: '../img/w/erc-panchamana-garden.jpg',
    focus: '50% 50%'
  },
  {
    slug: 'advanced-programs-reopening',
    date: '2026-02-23',
    category: 'School Updates',
    title: 'Soil Food Web School Advanced Programs Are Reopening!',
    author: '',
    image: '../img/uploads/loida-teaching-3.jpg',
    focus: '50% 40%'
  },
  {
    slug: 'obituary-dr-elaine-ingham',
    date: '2026-02-18',
    category: 'Foundation Update',
    title: 'Obituary for Dr. Elaine Ingham',
    author: '',
    image: '../img/w/copy-of-9.jpg',
    focus: '50% 35%',
    theme: 'legacy'
  },
  {
    slug: 'new-board-member-eric-feiler',
    date: '2026-02-17',
    category: 'Foundation Update',
    title: 'The Soil Food Web Welcomes a New Board Member – Eric Feiler',
    author: '',
    image: '../img/w/workshop-group-around-compost-pile.jpg',
    focus: '50% 45%'
  },
  {
    slug: '2025-in-review',
    date: '2025-12-30',
    category: 'Blog',
    title: '2025 in Review: A time of transition – honoring our founder and guiding spirit, building stronger community, and preparing for a bright future',
    author: '',
    image: '../img/uploads/mar25-group-photo.jpg',
    focus: '50% 45%'
  },
  {
    slug: 'living-legacy-webinar-series',
    date: '2025-11-03',
    category: 'Events',
    title: 'Join the Free Webinar Series: A Living Legacy — The Science of the Soil Food Web',
    author: '',
    image: '../img/uploads/elaine-behind-microscope.jpg',
    focus: '50% 40%',
    theme: 'legacy'
  },
  {
    slug: 'soil-health-week-pakistan',
    date: '2025-10-22',
    category: 'Events',
    title: 'Soil Health Week 2025: Wild Soils UK and TrashIt Bring the Soil Food Web Approach to Pakistan',
    author: '',
    image: '../img/w/erc-panchamana-treeplanting-3-fb-img-1666271008784.jpg',
    focus: '50% 50%'
  },
  {
    slug: 'foundation-launches-as-nonprofit',
    date: '2025-10-17',
    category: 'School Updates',
    title: 'Soil Food Web Foundation Launches as Nonprofit to Carry Forward Dr. Elaine Ingham’s Legacy',
    author: '',
    image: '../img/w/2-hands-clasped-holding-plant-roots.jpg',
    focus: '50% 50%'
  },
  {
    slug: 'retirement-dr-elaine-ingham',
    date: '2025-10-16',
    category: 'School Updates',
    title: 'Retirement Announcement: Dr. Elaine Ingham',
    author: '',
    image: '../img/w/elaine-with-sample-bag.jpg',
    focus: '50% 35%',
    theme: 'legacy'
  },
  {
    slug: 'october-2025-newsletter',
    date: '2025-10-09',
    category: 'Blog',
    title: 'October 2025 – Newsletter',
    author: '',
    image: '../img/w/hand-of-compost.jpg',
    focus: '50% 50%'
  },
  {
    slug: 'sacramento-food-knowledge-culture',
    date: '2025-09-23',
    category: 'Events',
    title: 'Help us celebrate food, knowledge and culture in Sacramento this September',
    author: '',
    image: '../img/w/carla-nicks-son-nick-eri-wild-soils-event-11-2024.jpg',
    focus: '50% 40%'
  }
];
