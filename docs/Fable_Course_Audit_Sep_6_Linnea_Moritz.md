# Fable Course Audit, Sep 6

Prepared by Linnea Moritz, 6 September 2026.
Sixty-four inconsistencies and fixes found across soilfoodweb.com and school.soilfoodweb.com, grouped by page. Items marked **[decision]** need a decision from Evan; everything else is a straight edit. Each item has the problem, the fix, and why it matters to someone deciding whether to hand over money.

---

## Homepage
https://soilfoodweb.com

1. Hero button "Learn More" on https://soilfoodweb.com links to https://soilfoodweb.com/foundation-courses-2/, a legacy WordPress page last edited April 2025, instead of the Thinkific Foundation page https://school.soilfoodweb.com/bundles/soilfoodweb-foundation-courses. Fix: repoint to the Thinkific page. Why: this is the first click most visitors make. It drops them onto pre-restructure copy with old program names and a "Sign Up Now" that goes to https://www.soilfoodweb.com/product/foundation-courses/ and enrols into the old LMS (course pages like https://soilfoodweb.com/course/foundation-course-1-introduction-soil-food-web/, membership https://soilfoodweb.com/membership/foundation-course-all-access/). If they then open any Thinkific page they see a second version of the school with different names and numbers, and can't tell which one is real.

2. Footer banner "Become a Consultant 40% off FC + AP Bundle" on https://soilfoodweb.com appears with no explanation and no landing page; the adjacent link goes to https://school.soilfoodweb.com/courses/india-workshop-2026. **[decision]** Confirm what it is, who approved it, and whether it stays. Why: a visitor sees $4,999 at https://school.soilfoodweb.com/bundles/soilfoodweb-foundation-courses and $3,999 at https://school.soilfoodweb.com/bundles/complete-practicum, then 40% off both in the footer. The conclusion is that list prices aren't real. It also can't convert because there is nowhere to buy it; it's not on https://school.soilfoodweb.com/collections either.

3. "Become a Soil Food Web Consultant" section on https://soilfoodweb.com still says "join the Consultant Training Program". Replace with Advanced Programs. Why: CTP was retired, announced at https://soilfoodweb.com/soil-food-web-advanced-programs-reopen-2026/. The homepage says the next step is CTP; the menu has only "Advanced Programs" and https://school.soilfoodweb.com/bundles/complete-practicum, and that page's first FAQ calls CTP a "legacy name". The visitor has to guess whether these are the same thing. A homepage a year behind its own menu tells people the school isn't maintaining itself.

4. https://soilfoodweb.com carries "up to 150% increase in crop production", "up to 100% reduced chemical inputs", "up to 50% reduction in irrigation", "reverse climate change within 15 to 20 years", "recognized as the foremost soil biologist in the world", and the Shane Plath 150% yield testimonial (repeated on https://school.soilfoodweb.com/bundles/complete-practicum). **[decision]** Remove the numeric claims and superlative; replace with directory count from https://soilfoodweb.com/certified-listing-directory/ and graduate outcomes. Why: none of these link to a study, and https://soilfoodweb.com/publications/ doesn't support them either. A sceptical scientist, funder or journalist looks for the source, doesn't find it, and discounts everything else. Verifiable anchors exist: the directory, and Dr. Ingham's Google Scholar profile https://scholar.google.com/citations?user=iOm3z4AAAAAJ, which the site doesn't link anywhere.

5. Page title on https://soilfoodweb.com is "Dr. Elaine's™ Soil Food Web School" and og:title is "Home (new)". Fix both. Why: the title is what shows in Google results and browser tabs; og:title is what shows when the link is shared on LinkedIn or WhatsApp. "Home (new)" is a placeholder that went live, and "School" contradicts the Foundation named in the footer and at https://soilfoodweb.com/donations/.

6. Site name in metadata on https://soilfoodweb.com is still "Soil Food Web School - Regenerating Soil" while the footer says Foundation. Why: every shared link and search result names one organisation and the page footer names another.

## Navigation (every WordPress page)

7. Advanced Programs submenu reads "Field Trail", linking to https://school.soilfoodweb.com/bundles/advanced-field-trial. Should be "Field Trial". Why: a typo in the name of a $1,250 product, visible on every page of https://soilfoodweb.com.

8. Menu says "Soil Sponge Workshop (SSW)"; the page title and URL at https://soilfoodweb.com/soil-sponge-regeneration-workshop/ say Soil Sponge Regeneration Workshop (SSR). Pick one. Why: two acronyms for one product make a visitor wonder whether they are two products, and people searching for the name they saw in the menu don't find the page.

9. Nav has "Directory (NEW)" https://soilfoodweb.com/certified-listing-directory/ alongside the older https://soilfoodweb.com/consultants/ and https://soilfoodweb.com/laboratory-technicians/. Retire the old two once the directory is complete. Why: three places to find practitioners with different people on each. A farmer looking for a consultant doesn't know which list is current, and a prospective student can't tell how many graduates there are.

10. "Life in the Soils" two-day seminar https://school.soilfoodweb.com/courses/life-in-the-soils-seminar-2-day is sold as a prerequisite on https://school.soilfoodweb.com/courses/india-workshop-2026 but appears in no menu and not on https://school.soilfoodweb.com/collections. Why: the India page tells people they must complete either the Foundation Courses or this seminar. Anyone who wants the cheaper route can't find it from the site.

## Legacy Foundation Courses page
https://soilfoodweb.com/foundation-courses-2/

11. "Sign Up Now" on https://soilfoodweb.com/foundation-courses-2/ goes to the WooCommerce product https://www.soilfoodweb.com/product/foundation-courses/ which enrols into the old WordPress LMS, while the nav link goes to https://school.soilfoodweb.com/bundles/soilfoodweb-foundation-courses with checkout at https://school.soilfoodweb.com/enroll/3692699. Two live checkouts for the same course into two delivery systems. **[decision]** Choose one and redirect the other. Why: a student who buys through WooCommerce lands in a different platform from one who buys through Thinkific, with different forums, logins and support paths. Enrolment data is split, so nobody can see true numbers.

12. https://soilfoodweb.com/foundation-courses-2/ still says Consultant Training Program, "some graduates charge around $150 per hour", "over 5 million acres", and "regular price is $5,000". Why: CTP is retired (see https://soilfoodweb.com/soil-food-web-advanced-programs-reopen-2026/); $150 per hour is an unsourced income claim; 5 million acres can't be verified; and $5,000 contradicts $4,999 on https://school.soilfoodweb.com/bundles/soilfoodweb-foundation-courses and https://www.soilfoodweb.com/product/foundation-courses/.

13. https://soilfoodweb.com/foundation-courses-2/ holds the useful facts missing from Thinkific: ~150 hours to complete, four weeks full time, 12-month limit, refund valid if 30 lectures or fewer watched, ten FAQs, and the full lecture list at https://drive.google.com/file/d/1UPKCBfaR0i58HPGOLJavYB7SrkJTlADN/view?usp=sharing. Migrate these to https://school.soilfoodweb.com/bundles/soilfoodweb-foundation-courses before retiring this one. Why: these are the answers a serious buyer needs. They live on the page that should come down, so retiring it without moving them makes the flagship page worse.

14. https://www.soilfoodweb.com/product/foundation-courses/ describes the course as "over 40 hours of lectures"; https://soilfoodweb.com/foundation-courses-2/ says 150 hours of study. Publish one figure for lecture hours and one for total study time. Why: both may be true for different things, but nobody says which, so the reader sees two contradictory numbers for the same course.

15. https://www.soilfoodweb.com/product/foundation-courses/ offers a payment plan via https://soilfoodweb.com/product/the-soil-food-web-foundation-courses-1st-payment/; https://school.soilfoodweb.com/bundles/soilfoodweb-foundation-courses offers none. **[decision]** Payment plan yes or no, and on which platform. Why: $4,999 upfront is the biggest reason people don't buy. A plan exists but only on the page being retired.

## Thinkific Foundation Courses page
https://school.soilfoodweb.com/bundles/soilfoodweb-foundation-courses

16. Headline on https://school.soilfoodweb.com/bundles/soilfoodweb-foundation-courses says 63 lectures; the modules listed on the same page total 59 + 22 + 26 + 32 + 73 = 212 lessons. Explain the relationship or fix the count. Why: the reader adds the numbers on the page and gets 212, not 63, and can't tell what they're buying.

17. https://school.soilfoodweb.com/bundles/soilfoodweb-foundation-courses has only three FAQs. No hours, no time limit, no refund terms (which live at https://soilfoodweb.com/terms/), no equipment note, no mention that https://school.soilfoodweb.com/bundles/complete-practicum ($3,999) follows. Add all of these. Why: at $4,999 people need to know what they're committing to. Discovering the second tier afterwards is what makes the pricing feel like a trap.

18. "Earn your awesome certificate / unlock your awesome certificate" on https://school.soilfoodweb.com/bundles/soilfoodweb-foundation-courses. Replace with what the certificate is and who issues it. Why: "awesome" is the language of a $30 hobby course on a $4,999 page. Compare how https://school.soilfoodweb.com/courses/permaculture-design-certification names its issuing body.

19. Total path cost ($4,999 at https://school.soilfoodweb.com/bundles/soilfoodweb-foundation-courses plus $3,999 at https://school.soilfoodweb.com/bundles/complete-practicum) is not stated on either page. State it. Why: everybody assumes $5,000 is the whole thing. Stating $8,998 up front removes the resentment.

20. https://school.soilfoodweb.com/bundles/soilfoodweb-foundation-courses says "automatically eligible to join our Advanced Programs" but the 90% gate appears only at the bottom; https://soilfoodweb.com/foundation-courses-2/ and https://school.soilfoodweb.com/bundles/complete-practicum both state it clearly. Put the gate up front. Why: finding out after payment that you need a 90% average to continue feels like the rules changed.

## Intro Mini Course
https://school.soilfoodweb.com/courses/intro-foundation-course

21. https://school.soilfoodweb.com/courses/intro-foundation-course says "ten lessons"; eleven titles are listed. Why: the reader counts and gets a different number from the headline, on the entry product.

22. https://school.soilfoodweb.com/courses/intro-foundation-course refers to the "$5,000 Foundations Course"; https://school.soilfoodweb.com/bundles/soilfoodweb-foundation-courses says $4,999. Why: two prices and two names ("Foundations" vs "Foundation") one click apart.

23. "$1,600 total value" stack on https://school.soilfoodweb.com/courses/intro-foundation-course includes "$100 value" for the public community, which https://school.soilfoodweb.com/collections and https://school.soilfoodweb.com/products/communities/SFW-public-community show as free. Remove the stack or make it true. Why: claiming a $100 value for something given away free is visible in two clicks and reads as an infomercial trick to exactly the audience that punishes it.

## Permaculture Design Certification
https://school.soilfoodweb.com/courses/permaculture-design-certification

24. No price on https://school.soilfoodweb.com/courses/permaculture-design-certification. https://school.soilfoodweb.com/collections shows $1,550. Add it. Why: a course page with no price makes people assume it's expensive or leads to a sales call, and the price is already public one page away.

25. https://school.soilfoodweb.com/courses/permaculture-design-certification says 12 weeks in one place and 13 weeks in another. Why: a live cohort course must state its length exactly; people arrange work and childcare around it.

26. Typos on https://school.soilfoodweb.com/courses/permaculture-design-certification: "Soil Fodo Web", "renegerative", "Malasia". Why: the organisation's own name misspelled on the page for its only externally accredited course, the page you'd otherwise hold up as the model. The launch post at https://soilfoodweb.com/soil-food-web-school-first-permaculture-design-certificate-course/ links here.

27. Live session times on https://school.soilfoodweb.com/courses/permaculture-design-certification say "Pacific / California Time" without PDT or PST; cohort runs 16 Sept to 20 Dec, crossing the November clock change. Why: international students miss sessions by an hour after the change, and 80% attendance is a graduation requirement on the same page.

28. Kavi Reddy's bio on https://school.soilfoodweb.com/courses/permaculture-design-certification says "Director of Operations at the Soil Food Web School"; https://school.soilfoodweb.com/courses/india-workshop-2026 lists her as "Growth, Partnerships, and Permaculture". Confirm and use one. Why: two titles for the same person; a funder doing due diligence on who runs the organisation will notice. Check against https://soilfoodweb.com/about/.

## Introduction to Ecosystem Restoration
https://school.soilfoodweb.com/bundles/introduction-to-ecosystem-restoration

29. https://school.soilfoodweb.com/bundles/introduction-to-ecosystem-restoration lists modules at 73, 73, 72, 73 lessons (291) against "approximately 80 hours of study". Reconcile. Why: 291 lessons in 80 hours is 16 minutes each; the reader can't picture the workload.

30. Refund condition on https://school.soilfoodweb.com/bundles/introduction-to-ecosystem-restoration says "less than half the lectures (under 16 hours)", implying a 32-hour course. Reconcile with the 80-hour claim. Why: the refund rule contradicts the course length on the same page.

## Soil Sponge Workshop
https://soilfoodweb.com/soil-sponge-regeneration-workshop/

31. Only dates on https://soilfoodweb.com/soil-sponge-regeneration-workshop/ are 3 Feb to 3 Mar 2026, already run. Registration is still live at https://soilfoodweb.com/product/regenerating-the-soil-sponge/. **[decision]** Publish next cohort dates or take the buy button down. Why: someone can pay $300 today for a workshop whose only listed dates are in the past.

32. https://soilfoodweb.com/soil-sponge-regeneration-workshop/ sends graduates to a follow-on community on Teachable, a fourth platform after https://soilfoodweb.com, https://school.soilfoodweb.com and https://webinar.soilfoodweb.com/. Note for the platform consolidation conversation. Why: every extra platform is another login for students and another thing that breaks when Alex goes part-time.

## Complete Practicum
https://school.soilfoodweb.com/bundles/complete-practicum

33. "Gain globally recognized validation with your certificate of completion" on https://school.soilfoodweb.com/bundles/complete-practicum names no recognising body. **[decision]** Replace with: issued by Soil Food Web Foundation, not externally accredited, confers a listing at https://soilfoodweb.com/certified-listing-directory/. Why: "recognised by whom?" has a checkable answer, and it's nobody outside SFW. Compare https://school.soilfoodweb.com/courses/permaculture-design-certification, which names the Permaculture Association.

34. On https://school.soilfoodweb.com/bundles/complete-practicum FAQ 1 says CTP and CLP are legacy names; the partners FAQ on the same page says "You must be an enrolled CTP student to take part in any meeting." Fix the second. Why: the same page says CTP no longer exists and that you must be enrolled in it.

35. "Every AP Course provides..." on https://school.soilfoodweb.com/bundles/complete-practicum. Write Advanced Program in full. Why: Advanced Placement is a US college-credit system; an American reader may assume college credit, an accreditation implication SFW isn't claiming.

36. Time investment answer on https://school.soilfoodweb.com/bundles/complete-practicum gives only "42 months allotted"; https://school.soilfoodweb.com/courses/india-workshop-2026 says compost alone typically takes 18 to 24 months. State a typical completion range. Why: "42 months allotted" is a deadline, not a duration. Someone planning a career change currently finds the real figure only in a different product's FAQ.

37. Testimonials on https://school.soilfoodweb.com/bundles/complete-practicum include the 150% yield claim and "saved them over $1M" (also on https://soilfoodweb.com). **[decision]** Swap for testimonials describing what the graduate now does, sourced from https://soilfoodweb.com/certified-listing-directory/ and the video testimonials at https://soilfoodweb.com/resources/testimonials-videos/. Why: these are unverifiable claims about farms, not students, and the kind that gets quoted back at the organisation. "I did this course and now I run a lab in Scotland" is checkable.

38. "Mentorship Without Limits / no clock, no hours counted" on https://school.soilfoodweb.com/bundles/complete-practicum. **[decision]** Confirm mentor capacity supports this. Why: the old CTP capped mentoring at 56 hours; "unlimited" is a written promise to every student for 42 months. If hours are rationed in practice, it's a refund dispute.

39. Equipment cost (~$1,000) on https://school.soilfoodweb.com/bundles/complete-practicum appears only in the FAQ; the full spec is on https://school.soilfoodweb.com/bundles/advanced-soil-microscopy. Move it above the price. Why: it's a real cost of taking the course. Finding it after the price is the same pattern as the hidden second tier.

40. Prerequisites on https://school.soilfoodweb.com/bundles/complete-practicum list "access to a microscope and compatible camera", but https://school.soilfoodweb.com/bundles/advanced-biocomplete-compost-production says microscopy is no longer required to start Compost. Clarify. Why: someone who wants compost skills without $1,000 of equipment reads two pages and gets two answers.

## Advanced Soil Microscopy
https://school.soilfoodweb.com/bundles/advanced-soil-microscopy

41. Meta description of https://school.soilfoodweb.com/bundles/advanced-soil-microscopy states Lab-Tech status must be re-tested every 12 months; it appears nowhere in the visible page. **[decision]** Confirm whether recertification is enforced; if yes, put it on the page; if no, remove it. Why: a recurring obligation attached to a credential must be known before paying. Right now only people who read the Google snippet know. If it's enforced, graduates listed at https://soilfoodweb.com/certified-listing-directory/ who didn't know may lose status they paid for.

42. Enrolment requirements FAQ on https://school.soilfoodweb.com/bundles/advanced-soil-microscopy still says "be enrolled in CLP, CTP or GTP", programs the same page and https://school.soilfoodweb.com/bundles/complete-practicum call legacy. Why: a reader is told to enrol in programs that don't exist.

43. Payment plan on https://school.soilfoodweb.com/bundles/advanced-soil-microscopy is 6 × $250 = $1,500 against $1,250 upfront; the $250 premium is stated but not explained. Same on https://school.soilfoodweb.com/bundles/advanced-biocomplete-compost-production and https://school.soilfoodweb.com/bundles/advanced-biological-liquid-amendments. Why: a 20% surcharge for paying monthly reads as a penalty on people who can't pay upfront, which sits badly with a charity at https://soilfoodweb.com/donations/.

## Advanced BioComplete Compost Production
https://school.soilfoodweb.com/bundles/advanced-biocomplete-compost-production

44. https://school.soilfoodweb.com/bundles/advanced-biocomplete-compost-production says 10 months allotted; prerequisites on the same page say "build three compost piles within 16 months". Reconcile. Why: the deadline is shorter than the window for the course's own core task.

45. Same CTP contradiction on https://school.soilfoodweb.com/bundles/advanced-biocomplete-compost-production as on https://school.soilfoodweb.com/bundles/complete-practicum (FAQ says legacy, later FAQ says "must be an enrolled CTP student"). https://school.soilfoodweb.com/bundles/advanced-soil-microscopy fixed this line. Why: the inconsistency is now between pages as well as within them.

## Advanced Biological Liquid Amendments
https://school.soilfoodweb.com/bundles/advanced-biological-liquid-amendments

46. The "Can I select a mentor of my preference?" answer on https://school.soilfoodweb.com/bundles/advanced-biological-liquid-amendments contains Thinkific's default placeholder text, including the instruction to delete it. Fix today. Why: a $1,250 product page telling the reader "delete this placeholder and add your content". The correct answer already exists on https://school.soilfoodweb.com/bundles/complete-practicum; copy it.

47. https://school.soilfoodweb.com/bundles/advanced-biological-liquid-amendments requires both https://school.soilfoodweb.com/bundles/advanced-soil-microscopy and https://school.soilfoodweb.com/bundles/advanced-biocomplete-compost-production first, contradicting the removal of sequencing described on https://school.soilfoodweb.com/bundles/complete-practicum and https://soilfoodweb.com/soil-food-web-advanced-programs-reopen-2026/. **[decision]** State it's sequential or remove the prerequisite. Why: someone who bought Compost first expecting to choose their own order finds a gate they weren't told about.

## Advanced Field Trial
https://school.soilfoodweb.com/bundles/advanced-field-trial

48. https://school.soilfoodweb.com/bundles/advanced-field-trial lists no prerequisites, while https://school.soilfoodweb.com/courses/india-workshop-2026 lists Field Trial entry requirements (200-gallon pile meeting biological minimums, remote compost assessment) and points to https://drive.google.com/file/d/1yKlyLtFCrQVkaFlGNU_9wTDKrPzdz_xt/view?usp=sharing. Add them here. Why: the capstone course that confers Consultant status has no stated entry requirements on its own page. A buyer can pay $1,250 and then be told they can't start.

49. Three prices on https://school.soilfoodweb.com/bundles/advanced-field-trial: $1,250 upfront, 8 × $125 = $1,000, 6 × $250 = $1,500. The 8-payment plan is cheaper than upfront. **[decision]** Almost certainly an error. Why: paying over eight months costs less than paying today, contradicting the "pay upfront and save" logic on https://school.soilfoodweb.com/bundles/advanced-soil-microscopy.

## India Accelerator Workshop
https://school.soilfoodweb.com/courses/india-workshop-2026

50. "Early Nematode Discount available through Monday, August 10" is still displayed on https://school.soilfoodweb.com/courses/india-workshop-2026, expired. Why: an expired deadline on a live page tells the reader it isn't maintained, and anyone who asks for it creates a support conversation.

51. On https://school.soilfoodweb.com/courses/india-workshop-2026 inclusions say "13 nights", the room section says "12 nights", the FAQ says Sunday 18 to Saturday 31 October (13 nights). Reconcile, and check against the handbook at https://drive.google.com/file/d/1V08HBj3axtJjlAhycwgmzuGj3Yr9Bosx/view?usp=drive_link. Why: people book flights around this.

52. Cancellation deadline on https://school.soilfoodweb.com/courses/india-workshop-2026 is 7 September 2026, per the participation agreement https://drive.google.com/file/d/1yKlyLtFCrQVkaFlGNU_9wTDKrPzdz_xt/view?usp=sharing. Not an error; make sure someone is watching it. Why: any cancellation on the 8th becomes a dispute unless the date is in front of someone. Future-cohort interest goes to https://school.soilfoodweb.com/pages/workshop-interest.

53. https://school.soilfoodweb.com/courses/india-workshop-2026 is the only page that states how long the Practicum really takes (18 to 24 months for compost). Whatever number goes here should match https://school.soilfoodweb.com/bundles/complete-practicum and https://school.soilfoodweb.com/bundles/advanced-biocomplete-compost-production. Why: the workshop pitch is "18 to 24 months in two weeks". If the Practicum page states a different duration, one pitch is wrong.

## Courses Overview
https://soilfoodweb.com/sfw-courses-overview/

54. https://soilfoodweb.com/sfw-courses-overview/, linked from the nav as the course overview, contains no course list, no prices, no prerequisites, and no mention of the Advanced Programs; its only button goes to https://school.soilfoodweb.com/bundles/soilfoodweb-foundation-courses. **[decision]** Rebuild as the actual overview or remove from the nav. Why: someone clicks "Courses Overview" expecting the courses and gets a video, a testimonial and one button. The full structure exists only in the dropdown menu.

## Directory
https://soilfoodweb.com/certified-listing-directory/

55. https://soilfoodweb.com/certified-listing-directory/ is not linked from https://school.soilfoodweb.com/bundles/soilfoodweb-foundation-courses, https://school.soilfoodweb.com/bundles/complete-practicum, or any Advanced page, and the total count isn't stated anywhere. Pull the number and put it on every course page. Why: it's the strongest proof that graduates go on to work: named people, named businesses, 45 countries. A prospective student asking "will this get me hired" never sees it.

56. Several Dutch entries on https://soilfoodweb.com/certified-listing-directory/ show country as "Netherlands Antilles" (Eindhoven, Wijk bij Duurstede, The Hague). Why: the Netherlands Antilles was dissolved in 2010 and was in the Caribbean. A Dutch farmer filtering by country won't find these consultants.

57. Profile images on https://soilfoodweb.com/certified-listing-directory/ uploaded as .heic and .tif (Davis Limbach, Nicholas Matteis, Tony Terusa) won't render in most browsers. Why: those listings show a broken image and the directory looks unfinished.

58. Name typos on https://soilfoodweb.com/certified-listing-directory/: "Catheirne Mac Rae", "Christopher Carlislle", "Christine Lenches-HInkel". Check with the practitioners before editing. Why: a client searching by the correct name won't find them, and the practitioner's own credential page misspells them.

59. Some profile photos on https://soilfoodweb.com/certified-listing-directory/ are still served from the old CLP platform, e.g. https://clp.soilfoodweb.com/assets/uploaded/students/directory/directory-profile-1887_2a0edf2374864109b913f5794fb405e1.jpg. If that subdomain is decommissioned, those images break. Why: a hidden dependency on a legacy system nobody will remember when it's switched off.

## Legal and entity naming

60. https://soilfoodweb.com/privacy-policy/ and https://soilfoodweb.com/terms/ name Soil Foodweb School LLC throughout; the footer of https://soilfoodweb.com says Soil Food Web Foundation, 501(c)(3), EIN 39-4439236; https://school.soilfoodweb.com/collections and every Thinkific page say "© Copyright Soil Food Web School 2026". **[decision]** Legal review of which entity the enrolment agreement is with, then one name everywhere. Why: a student paying $4,999 is entering a contract and the site names three counterparties. A donor at https://soilfoodweb.com/donations/ sees a privacy policy from an LLC. A funder will ask which entity holds the money and the obligations.

61. https://soilfoodweb.com/terms/ says no refund once 31 or more Foundation lectures are accessed; https://soilfoodweb.com/foundation-courses-2/ says "watched 30 lectures or less"; https://school.soilfoodweb.com/bundles/soilfoodweb-foundation-courses states neither. Put the rule on the page where people buy. Why: a refund request becomes an argument about a rule the buyer never saw.

## Cross-cutting

62. GTP (Grower Training Program) is called retired on https://school.soilfoodweb.com/courses/india-workshop-2026 ("formerly Stage 1 of the CTP/GTP") and on https://school.soilfoodweb.com/bundles/advanced-soil-microscopy, with no successor named anywhere, including https://soilfoodweb.com/soil-food-web-advanced-programs-reopen-2026/. **[decision]** Say what a grower who isn't aiming for consultant status should buy. Why: farmers who just want to fix their own land are a major audience and the product for them vanished without a named replacement.

63. https://school.soilfoodweb.com/bundles/complete-practicum ($3,999) costs less than https://school.soilfoodweb.com/bundles/soilfoodweb-foundation-courses ($4,999) that gates it, with no explanation on either page. **[decision]** Structural. Why: video lectures with no mentor cost more than 42 months of one-on-one mentoring, and nobody can explain that to a buyer because there's no explanation.

64. Four platforms in the purchase path: https://soilfoodweb.com (WordPress/WooCommerce, e.g. https://soilfoodweb.com/product/regenerating-the-soil-sponge/), https://school.soilfoodweb.com (Thinkific), https://webinar.soilfoodweb.com/, and Teachable via https://soilfoodweb.com/soil-sponge-regeneration-workshop/. Plus the affiliate site https://partners.soilfoodweb.com and the legacy https://clp.soilfoodweb.com. **[decision]** Consolidation plan tied to the Alex transition. Why: every platform is a separate login for students, a separate admin for staff, and a separate thing only Alex knows how to fix. Most of the inconsistencies above exist because the same fact has to be maintained in several places.
