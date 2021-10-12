plugins {
    kotlin("jvm")
}

tasks {
    jar {
        archiveBaseName.set("yat-${project.name}")
    }
}

dependencies {
    implementation(project(":yat:sql-parser"))
    implementation(project(":yat:schedule-parser"))
    implementation(project(":yat:compatible"))
    implementation(project(":yat:common"))
    implementation(project(":yat:report"))
    implementation(project(":yat:diff"))
    implementation(project(":yat:setting"))
    implementation("org.junit.jupiter:junit-jupiter-api:5.8.0")
    implementation("org.junit.jupiter:junit-jupiter-engine:5.8.0")

    implementation("org.junit.platform:junit-platform-launcher:1.7.2")
    implementation("commons-codec:commons-codec:1.15")
    implementation("org.jetbrains.kotlin:kotlin-stdlib-jdk8")
    implementation("org.jetbrains.kotlin:kotlin-reflect")
    implementation("org.slf4j:slf4j-api:1.7.32")
    implementation("ch.qos.logback:logback-classic:1.2.5")
    implementation("org.codehaus.groovy:groovy:3.0.8")
    implementation("org.spockframework:spock-core:2.0-groovy-3.0")
}

