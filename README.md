Node.js + Express web-app that lets users upload their DWeb Camp images to a scrapbook hosted on archive.org.

---

#### Functionality Goals

In preparation for future dweb camps, we have to ask ourselves what functionality is most important and which
design philosophies we want to follow.

The internet archive stores a group of photos as an individual item, which isn't very useful for sorting through them
categorically or by date. I noticed in [the category for last years event](https://archive.org/details/dwebcamp2019)
that others had grouped their photos by which day of the event they were taken. Perhaps instead of uploading all photos
in one 'item' on the archive, they could be synced at the end of each night into their own items depending on the day.

If we group by day, there's no reason we couldn't categorise things in other ways too. If we let people specify if an
image/video was created during a Lightning Talk or some other activity, and there's a significant amount of photos for
each category, then there's no reason they couldn't be grouped into a few different items for each day. Anything without
a specified category or event can just go in one big 'other' group.

So ultimately, the script could end up uploading photos in groups with a structure like "dweb2020 \[day\] \[event\]".
Build days and actual camp days will be separated, of course.

Now, I'm not sure how flexible the API is for these things, but it's likely people will forget to upload their photos on
the day they were taken, or they might upload all of them at the end. If the API allows us to edit and add images to
pre-existing items on the archive, then we may be able to just read photo metadata to determine which folder it should
be uploaded in based on the date.
