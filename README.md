gitlab-tools
============

## report-docker-registry

Gives you a report over all container registry images.

**Warning:** Sizes are summed up and usually are way higher than the stored size on disk. 

**Example:**

```
## magicunicorn

magicunicorn/gomagic:latest	336.6MiB
magicunicorn/docker-something:latest	523.9MiB
magicunicorn/docker-foobar:latest	210.2MiB

Total for group: 1.0GiB

....

## Total

133.6GiB
```

## Copyright

Copyright (C) 2020 [Markus Frosch](mailto:markus@lazyfrosch.de)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see [gnu.org/licenses](http://www.gnu.org/licenses/).
