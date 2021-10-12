plugins {
    java
    kotlin("jvm")
}

dependencies {
    compileOnly("org.projectlombok:lombok:1.18.6")
    annotationProcessor("org.projectlombok:lombok:1.18.6")
    implementation("org.jetbrains.kotlin:kotlin-stdlib-jdk8")

    testImplementation("org.junit.jupiter:junit-jupiter-api:5.8.0")
    testRuntimeOnly("org.junit.jupiter:junit-jupiter-engine:5.8.0")
}

tasks {
    jar {
        archiveBaseName.set("yat-${project.name}")
    }

    test {
        useJUnitPlatform()
    }
}

