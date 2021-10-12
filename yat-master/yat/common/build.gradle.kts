plugins {
    kotlin("jvm")
}

dependencies {
    compileOnly("org.projectlombok:lombok:1.18.6")
    annotationProcessor ("org.projectlombok:lombok:1.18.6")

    implementation("org.jetbrains.kotlin:kotlin-stdlib-jdk8")
    implementation("org.slf4j:slf4j-api:1.7.32")
}

tasks {
    jar {
        archiveBaseName.set("yat-${project.name}")
    }
}
