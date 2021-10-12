plugins {
    kotlin("jvm")
}

dependencies {
    implementation(project(":yat:common"))
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

