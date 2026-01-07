import struct
import os

def extract_wavs_from_bin(bin_path='se.bin', output_dir='soundeffects'):
    if not os.path.isfile(bin_path):
        print(f"Error: File '{bin_path}' not found.")
        return

    with open(bin_path, 'rb') as f:
        data = f.read()

    riff_signature = b'RIFF'
    wave_signature = b'WAVE'
    count = 0
    offset = 0
    total_len = len(data)

    os.makedirs(output_dir, exist_ok=True)

    while offset < total_len:
        riff_index = data.find(riff_signature, offset)
        if riff_index == -1:
            break

        if riff_index + 12 > total_len:
            break

        # Check if WAVE follows the RIFF chunk
        if data[riff_index + 8:riff_index + 12] != wave_signature:
            offset = riff_index + 4
            continue

        # Read size (little-endian uint32)
        size_bytes = data[riff_index + 4:riff_index + 8]
        size = struct.unpack('<I', size_bytes)[0]
        wav_total_size = size + 8

        if riff_index + wav_total_size > total_len:
            print(f"Warning: WAV at offset {riff_index} exceeds file size. Skipping.")
            offset = riff_index + 4
            continue

        wav_data = data[riff_index:riff_index + wav_total_size]

        out_filename = os.path.join(output_dir, f'extract_{count:03}.wav')
        with open(out_filename, 'wb') as out_file:
            out_file.write(wav_data)

        print(f"Extracted: {out_filename} ({wav_total_size} bytes)")

        offset = riff_index + wav_total_size
        count += 1

    if count == 0:
        print("No WAV files found in the binary.")
    else:
        print(f"\nDone. {count} WAV files extracted to '{output_dir}'.")

# Run the function when this script is executed
if __name__ == '__main__':
    extract_wavs_from_bin()