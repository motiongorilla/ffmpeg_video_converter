import subprocess

ffmpeg: str = "/usr/bin/ffmpeg"


def userInput() -> dict:
    def filterInput(message, default):
        user_input = input(message)

        if user_input == "":
            user_input = default
        return user_input

    print("Press Enter for defaults \n")

    input_dict: dict = {}

    input_dict["input_file"] = filterInput("Input file: ", "")
    input_dict["output_file"] = filterInput(
        "Output file (default ./clip.mp4): ", "./clip.mp4"
    )
    input_dict["video_codec"] = filterInput(
        "Video codec (default libx265): ", "libx265"
    )
    input_dict["audio_codec"] = filterInput("Audio codec (default aac): ", "aac")
    input_dict["audio_bitrate"] = filterInput("Audio bitrate (default 196k): ", "196k")
    input_dict["sample_rate"] = filterInput("Sample rate (default 44100): ", "44100")
    input_dict["encoding_speed"] = filterInput(
        "Encoding speed (default fast): ", "fast"
    )
    input_dict["crf"] = filterInput("Constant Rate Factor (default 22): ", "22")
    input_dict["frame_size"] = filterInput(
        "Frame size (default 1920x1080): ", "1920x1080"
    )

    return input_dict


def buildFfmpegCommand() -> list:
    user_input = userInput()
    command: list = [
        ffmpeg,
        "-i",
        user_input["input_file"],
        "-c:v",
        user_input["video_codec"],
        "-preset",
        user_input["encoding_speed"],
        "-crf",
        user_input["crf"],
        "-s",
        user_input["frame_size"],
        "-c:a",
        user_input["audio_codec"],
        "-b:a",
        user_input["audio_bitrate"],
        "-ar",
        user_input["sample_rate"],
        "-pix_fmt",
        "yuv420p",
        user_input["output_file"],
    ]

    return command


def runFfmpeg(commands):
    print(commands)

    if subprocess.run(commands).returncode == 0:
        print("FFMpeg ran succesfully!")
    else:
        print("There was an error during execution!")


# runFfmpeg(buildFfmpegCommand())
a = subprocess.run(
    [ffmpeg, "-i", "./src/VTB_video.mp4", "-hide_banner"], capture_output=True
)
# print(str(a.stderr).split("\\n")[7].split("Video: ")[1].split(",")[4].strip(""))
