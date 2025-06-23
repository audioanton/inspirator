function getNewWord() {

    fetch('/inspirator/word')
        .then(response => response.json())
        .then(data => {
            document.getElementById("text").setAttribute("value", data)
        })
        .catch((error) => {
            console.error('Error:', error)
        })
}

function getNewSounds() {

    fetch(('/inspirator/new_sounds'))
        .then(response => response.json())
        .then(data => {
            const table = document.getElementById("sounds")
            if (data.length === 0) {
                table.nextElementSibling.textContent = "No more sounds, search again!"
            } else {
                document.querySelectorAll(".sound-row").forEach( sound => sound.remove())
                const sounds = data.map(sound => getSoundElement(sound))
                sounds.forEach(soundRow => table.appendChild(soundRow))
            }
        })
        .catch((error) => {
        console.log(error)
    })
}

function getSoundElement(sound) {
    const audio = document.createElement("audio")
    audio.controls = true
    audio.src = `/inspirator/stream/${sound[0]}/${sound[2]}}`

    const source = document.createElement("td")
    source.append(audio)

    const title = document.createElement("td")
    title.textContent = sound[1]

    const fileType = document.createElement("td")
    fileType.textContent = sound[2]

    const seconds = document.createElement("td")
    seconds.textContent = sound[3]

    const size = document.createElement("td")
    size.textContent = sound[4]

    const button = document.createElement("button")
    button.textContent = "Download"

    const link = document.createElement("a")
    link.href = `/inspirator/download/${sound[0]}/${sound[1]}/${sound[2]}`
    link.append(button)

    const download = document.createElement("td")
    download.append(link)

    const row = document.createElement("tr")
    row.classList.add("sound-row")
    row.append(source, title, fileType, seconds, size, download)

    return row
}

const output = document.getElementById("outputLength")
const slider = document.getElementById("slider")

output.textContent = slider.value

slider.addEventListener("input", (event) => {
    output.textContent = event.target.value
})