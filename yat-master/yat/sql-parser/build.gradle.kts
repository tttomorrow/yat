
plugins {
    kotlin("jvm")
}

dependencies {
    implementation("org.jetbrains.kotlin:kotlin-stdlib-jdk8")
    implementation(project(":yat:common"))

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
