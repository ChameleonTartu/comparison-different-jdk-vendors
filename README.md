# Kotlin + Docker. Is OpenJDK the perfect image for production?

In this presentation, you will see available vendors in conemporary Java world, as an example I do it for JDK 11. We make comparison by image sizes, and performance of running image. As an example, I will take sample Spring Boot + Kotlin application.


## List of vendors to compare with

- [AdaptOpenJDK](https://hub.docker.com/r/adoptopenjdk/openjdk11)
- [Amazon](https://hub.docker.com/_/amazoncorretto)
- [Azul Zulu](https://hub.docker.com/r/azul/zulu-openjdk-alpine)
- [Bellsoft](https://hub.docker.com/r/bellsoft/liberica-openjdk-alpine)
- [SAP](https://hub.docker.com/_/sapmachine)
- [TravaOpenJDK](https://hub.docker.com/r/travactory/docker-openjdk11-kubectl)

Some other vendors are not covered as they have restricted licenses or under another set of technologies set. For instance, GraalVM is a separate discussion track.

## Size comparison

All images are taken with alpine Linux, if this distribution was available for comparison.

See results in [Sizes comparison report](comparison/generated_sizes_report.html)

## Performance comparison

To compare performance and stats among different openjdk images, we have used `Locust` load testing framework.

```
poetry run locust -f load_test.py -u 500 -r 10 --host http://localhost:8085
```

Images themselves were constrained to use as much RAM as they require but bounded by 2 cores only.

```
docker run -p8085:8085 --cpuset-cpus="0,1" -d bellsoft_liberica-openjdk-alpine-musl:11
```

Reports for each distribution are available under `stats/docker/<image_name>` paths.


| Image.         | Total # of requests     | Avg time (ms)     |
| :------------- | :----------: | -----------: |
| amazoncorretto:11 | 845   | 259728    |
| amazoncorretto:11-alpine   | 818 | 248999 |
| azul_zulu-openjdk-alpine:11-jre | 833 | 238408 |
| bellsoft_liberica-openjdk-alpine-musl:11 | 834 | 244292 |
| bellsoft_liberica-openjdk-alpine:11 | 789 | 245254 |
| sapmachine:11 | 760 | 249115 |
| travactory_docker-openjdk11-kubectl:latest | 759 | 258456 |
| adoptopenjdk_openjdk11:alpine | 805 | 242200 |
| azul_zulu-openjdk:11 | 574 | 278204 |
| azul_zulu-openjdk-alpine:11 | 831 | 259710 |
| amazoncorretto:11-alpine-jdk | 688 | 250009 |
| adoptopenjdk_openjdk11-openj9:alpine | 259 | 331422 |


## Summary

Size winner: `bellsoft/liberica-openjdk-alpine-musl:11`

Performance winners: `amazoncorretto:11`, `azul_zulu-openjdk-alpine:11-jre`, `bellsoft_liberica-openjdk-alpine-musl:11`

## Ranting about tools

- I had a great hope for [monolith single HTML download tool](https://github.com/Y2Z/monolith).
Unfortunately, it couldn't downloag GIFs from cAdvisor monitor.

- I wanted to find a nice tool for running Docker images monitoring. [cAdvisor](https://github.com/google/cadvisor) was supposed to be the tool. As I use it, I figured out that even it builds nice looking graphs, it doesn't do more than `docker stats`, so it is not possible to see image performance over the last N minutes.

## Recommendations

- Python dependency management tool [Poetry](https://python-poetry.org/) helped a lot in preliminary download of images and generating size report.

- Docker has did a job as always, no complaints. :-)




