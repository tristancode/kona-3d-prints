#!/bin/sh
# Tag every version commit ("rear: vN - ...", "front: vN - ...") as rear-vN / front-vN, then push the tags.
# Claude's cloud sessions cannot push tags, so run this from your own checkout.
set -e
git log --format='%H %s' | sed -n 's/^\([0-9a-f]*\) \(rear\|front\): v\([0-9]*\) - .*/\1 \2-v\3/p' |
while read sha tag; do git tag -f "$tag" "$sha"; done
git push origin --tags
