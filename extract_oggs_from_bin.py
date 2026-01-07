import os


def extract_oggs_from_bin(bin_path='bgm.bin', output_dir='bgm_oggs'):
    if not os.path.isfile(bin_path):
        print(f"Error: File '{bin_path}' not found.")
        return

    with open(bin_path, 'rb') as f:
        data = f.read()

    ogg_signature = b'OggS'
    count = 0
    offset = 0
    total_len = len(data)

    os.makedirs(output_dir, exist_ok=True)

    while offset < total_len:
        ogg_index = data.find(ogg_signature, offset)
        if ogg_index == -1:
            break

        # Gather full OGG stream until we hit an invalid page or EOF
        end_index = ogg_index
        last_valid = ogg_index

        while end_index < total_len:
            if data[end_index:end_index + 4] != ogg_signature:
                break

            if end_index + 27 > total_len:
                break  # not enough bytes for OGG header

            segment_count = data[end_index + 26]
            if end_index + 27 + segment_count > total_len:
                break

            segment_table = data[end_index + 27:end_index + 27 + segment_count]
            payload_size = sum(segment_table)
            page_total = 27 + segment_count + payload_size

            if end_index + page_total > total_len:
                break

            last_valid = end_index + page_total
            end_index = last_valid

        if last_valid > ogg_index:
            ogg_data = data[ogg_index:last_valid]
            out_filename = os.path.join(output_dir, f'extract_{count:03}.ogg')

            with open(out_filename, 'wb') as out_file:
                out_file.write(ogg_data)

            print(f"Extracted: {out_filename} ({len(ogg_data)} bytes)")

            count += 1

        offset = last_valid + 1

    if count == 0:
        print("No complete OGG files found in the binary.")
    else:
        print(f"\nDone. {count} OGG files extracted to '{output_dir}'.")


# Run the function when this script is executed
if __name__ == '__main__':
    extract_oggs_from_bin()
