import zlib
import struct
import math
import random
import os
import zipfile

def create_png(width, height, pixel_func):
    """Encodes 24-bit RGB PNG directly using standard zlib."""
    raw = bytearray()
    for y in range(height):
        raw.append(0)  # No PNG filter
        for x in range(width):
            r, g, b = pixel_func(x, y)
            raw.extend([
                max(0, min(255, int(r))),
                max(0, min(255, int(g))),
                max(0, min(255, int(b)))
            ])
    compressed = zlib.compress(bytes(raw), 9)
    ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', compressed) + chunk(b'IEND', b'')

def generate_all_images(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    size = 256
    cx, cy = 128, 128
    radius = 80

    # 1. Out-Of-Distribution: Tennis Ball (Yellow-green sphere with white seams)
    def img_tennis(x, y):
        dx = x - cx
        dy = y - cy
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > radius:
            return (242, 244, 247)  # neutral studio background
        # Seam curve: approx (x-cx)^2 / 30 - dy
        seam_dist1 = abs((dx*dx)/55.0 - dy - 20)
        seam_dist2 = abs(-(dx*dx)/55.0 - dy + 20)
        is_seam = min(seam_dist1, seam_dist2) < 4.0
        # Felt shading
        shade = 1.0 - (dist / radius) * 0.35 + (dy / radius) * 0.15 - (dx / radius) * 0.1
        noise = ((x * 17 + y * 31) % 19) / 80.0
        if is_seam:
            return (int(235 * shade), int(240 * shade), int(220 * shade))
        # Vibrant tennis felt yellow-green: RGB(205, 225, 30)
        r = (205 + noise * 20) * shade
        g = (228 + noise * 15) * shade
        b = (35 + noise * 10) * shade
        return (r, g, b)

    # 2. Out-Of-Distribution: Basketball (Pebbled burnt-orange sphere with black seams)
    def img_basketball(x, y):
        dx = x - cx
        dy = y - cy
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > radius:
            return (242, 244, 247)
        # Seam lines: vertical center, horizontal curve, side arcs
        is_vert_seam = abs(dx) < 2.5
        is_horiz_seam = abs(dy) < 2.5
        arc1 = abs(math.sqrt(max(0, (dx - 45)**2 + dy**2)) - 55) < 2.5
        arc2 = abs(math.sqrt(max(0, (dx + 45)**2 + dy**2)) - 55) < 2.5
        is_seam = is_vert_seam or is_horiz_seam or arc1 or arc2
        if is_seam:
            return (20, 20, 20)
        pebble = ((x % 4 == 0) and (y % 4 == 0)) * 25
        shade = 1.0 - (dist / radius) * 0.4 + (dy / radius) * 0.1 - (dx / radius) * 0.15
        # Burnt orange basketball color: RGB(225, 95, 20)
        r = (220 - pebble) * shade
        g = (95 - pebble * 0.6) * shade
        b = (20 - pebble * 0.2) * shade
        return (r, g, b)

    # 3. Texture Swap: Apple silhouette with banana peel yellow & speckles
    def img_texture_swap(x, y):
        dx = x - cx
        dy = y - (cy + 8)
        # Apple shape function: heart-dimple top and bottom
        r_apple = 75 + 6 * math.cos(math.atan2(dy, dx) * 2) - 12 * (1 if dy < -10 else 0) * (abs(dx)/40.0)
        dist = math.sqrt(dx*dx + dy*dy)
        # Stem
        if abs(x - cx) < 3.5 and 30 <= y <= 58:
            return (70, 45, 20)
        # Leaf
        ldx = x - (cx + 14)
        ldy = y - 48
        if ldx*ldx + ldy*ldy < 65 and ldx > 0:
            return (40, 140, 40)
        if dist > r_apple:
            return (242, 244, 247)
        # Banana yellow base with brown ripe spots
        speckle = ((x * 29 + y * 73) % 97 == 0) or ((x * 53 + y * 37) % 113 == 0)
        shade = 1.0 - (dist / r_apple) * 0.25 + (dy / r_apple) * 0.1
        if speckle:
            return (90 * shade, 60 * shade, 20 * shade)
        # Banana yellow: RGB(245, 215, 45)
        return (245 * shade, 218 * shade, 45 * shade)

    # 4. Adversarial Patch Sticker: Red apple with optical perturbation QR/grid sticker
    def img_patch_sticker(x, y):
        # Sticker bounding box: 145 to 195, 115 to 165
        if 145 <= x <= 195 and 115 <= y <= 165:
            # High-contrast geometric adversarial patch pattern
            px = (x - 145) // 5
            py = (y - 115) // 5
            val = ((px ^ py) * 7 + (px * py * 3)) % 11
            if val < 4:
                return (255, 255, 0)
            elif val < 8:
                return (0, 0, 220)
            else:
                return (240, 20, 20)
        dx = x - cx
        dy = y - (cy + 8)
        r_apple = 76 + 5 * math.cos(math.atan2(dy, dx) * 2)
        dist = math.sqrt(dx*dx + dy*dy)
        if abs(x - cx) < 3.5 and 30 <= y <= 56:
            return (70, 45, 20)
        if dist > r_apple:
            return (242, 244, 247)
        shade = 1.0 - (dist / r_apple) * 0.35 + (dy / r_apple) * 0.1
        # Crisp deep red apple
        return (215 * shade, 25 * shade, 30 * shade)

    # 5. High-Frequency Checkerboard Noise over Orange
    def img_frequency_noise(x, y):
        dx = x - cx
        dy = y - cy
        dist = math.sqrt(dx*dx + dy*dy)
        # Mathematical adversarial high-frequency noise
        noise_wave = (math.sin(x * 1.4) * math.cos(y * 1.4)) * 55.0
        if dist > radius:
            bg = 242 + noise_wave * 0.25
            return (bg, bg, bg)
        shade = 1.0 - (dist / radius) * 0.3
        r = (240 * shade) + noise_wave
        g = (125 * shade) - noise_wave * 0.8
        b = (20 * shade) + noise_wave * 1.2
        return (r, g, b)

    # 6. Inverted Negative Color Spectrum (Inverted Red Apple -> Cyan/Cobalt)
    def img_inverted_spectrum(x, y):
        dx = x - cx
        dy = y - (cy + 8)
        r_apple = 76 + 5 * math.cos(math.atan2(dy, dx) * 2)
        dist = math.sqrt(dx*dx + dy*dy)
        if abs(x - cx) < 3.5 and 30 <= y <= 56:
            return (255 - 70, 255 - 45, 255 - 20)
        if dist > r_apple:
            return (20, 22, 28)  # dark negative inverted background
        shade = 1.0 - (dist / r_apple) * 0.35
        # Invert of red (215, 25, 30) -> (40, 230, 225)
        return (40 * shade + 30, 220 * shade + 20, 240 * shade + 15)

    # 7. Camouflage & Background Blend (Orange on identical speckled orange texture)
    def img_camouflage(x, y):
        dx = x - cx
        dy = y - cy
        dist = math.sqrt(dx*dx + dy*dy)
        speckle = math.sin(x * 0.3) * math.cos(y * 0.3) * 35 + ((x*13 + y*17) % 23)
        if dist > radius:
            # Identical hue & texture in background
            return (230 + speckle * 0.4, 130 + speckle * 0.3, 30 + speckle * 0.2)
        # Faint boundary only
        edge_diff = 12 if abs(dist - radius) < 3 else 0
        return (235 + speckle * 0.4 + edge_diff, 135 + speckle * 0.3, 25 + speckle * 0.1)

    # 8. Chimeric Hybrid: Top half Orange slices, Bottom half Red Apple
    def img_chimeric(x, y):
        dx = x - cx
        dy = y - cy
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > radius:
            return (242, 244, 247)
        shade = 1.0 - (dist / radius) * 0.3
        if y < cy:
            # Top half: Orange segments & citrus pith
            angle = math.atan2(dy, dx)
            spoke = abs(math.sin(angle * 4)) < 0.12
            if spoke or dist < 12:
                return (248 * shade, 240 * shade, 220 * shade) # pith white
            return (245 * shade, 130 * shade, 15 * shade)
        else:
            # Bottom half: Solid crisp Apple red
            return (215 * shade, 22 * shade, 28 * shade)

    # 9. Out-Of-Distribution: Red Circular Traffic Signal Lens
    def img_traffic_light(x, y):
        dx = x - cx
        dy = y - cy
        dist = math.sqrt(dx*dx + dy*dy)
        # Outer dark housing
        if dist > radius + 15:
            return (242, 244, 247)
        if dist > radius:
            return (35, 38, 42) # dark matte metal rim
        # Fresnel lens texture rings
        fresnel = math.sin(dist * 0.7) * 20
        # Intense luminous red glow
        core_glow = max(0, 1.0 - (dist / radius)**2)
        r = min(255, 230 + core_glow * 25 + fresnel)
        g = min(255, 25 + core_glow * 35 + fresnel * 0.5)
        b = min(255, 20 + core_glow * 20)
        return (r, g, b)

    # 10. Extreme High-Contrast Silhouette (Backlit fruit shape, zero color)
    def img_silhouette(x, y):
        dx = x - cx
        dy = y - (cy + 5)
        r_shape = 75 + 4 * math.cos(math.atan2(dy, dx) * 3)
        dist = math.sqrt(dx*dx + dy*dy)
        if abs(x - cx) < 3 and 30 <= y <= 55:
            return (15, 15, 15)
        if dist > r_shape:
            # Blinding white background with lens flare rim
            rim = max(0, 1.0 - (dist - r_shape) / 10.0) * 120
            return (255, 255 - rim * 0.2, 255 - rim * 0.4)
        # Pitch black silhouette
        return (12, 14, 18)

    # 11. Out-of-Distribution: Green Apple Chameleon / Lizard texture
    def img_green_scales(x, y):
        dx = x - cx
        dy = y - (cy + 8)
        r_apple = 76 + 5 * math.cos(math.atan2(dy, dx) * 2)
        dist = math.sqrt(dx*dx + dy*dy)
        if abs(x - cx) < 3.5 and 30 <= y <= 56:
            return (70, 45, 20)
        if dist > r_apple:
            return (242, 244, 247)
        # Scaled hexagonal texture
        scale = ((int(x / 6) + int(y / 6)) % 2) * 30
        shade = 1.0 - (dist / r_apple) * 0.3
        return ((60 + scale) * shade, (185 - scale * 0.5) * shade, (40 + scale) * shade)

    # 12. Synthetic Cartoon Stylization (Extreme posterized minimalist lines)
    def img_posterized_banana(x, y):
        # Arc of banana
        angle = math.atan2(y - 80, x - cx)
        r_dist = math.sqrt((x - cx)**2 + (y - 80)**2)
        in_banana = 70 <= r_dist <= 115 and 0.4 <= angle <= 2.7
        # Stem tip
        in_tip = (abs(x - 65) < 8 and abs(y - 150) < 8) or (abs(x - 190) < 8 and abs(y - 150) < 8)
        if in_tip:
            return (60, 40, 20)
        if in_banana:
            # Flat posterized 3-step cell-shaded yellow
            step = 255 if r_dist < 85 else (225 if r_dist < 100 else 180)
            return (step, int(step * 0.88), 10)
        return (242, 244, 247)

    generators = [
        ("adv_01_ood_tennis_ball.png", img_tennis),
        ("adv_02_ood_basketball.png", img_basketball),
        ("adv_03_texture_swap_apple_banana.png", img_texture_swap),
        ("adv_04_adversarial_patch_sticker.png", img_patch_sticker),
        ("adv_05_checkerboard_frequency_noise.png", img_frequency_noise),
        ("adv_06_inverted_negative_spectrum.png", img_inverted_spectrum),
        ("adv_07_camouflage_background_blend.png", img_camouflage),
        ("adv_08_chimeric_sliced_hybrid.png", img_chimeric),
        ("adv_09_ood_traffic_light_red.png", img_traffic_light),
        ("adv_10_extreme_silhouette_backlit.png", img_silhouette),
        ("adv_11_ood_reptilian_scale_apple.png", img_green_scales),
        ("adv_12_posterized_minimal_banana.png", img_posterized_banana),
    ]

    for fname, gen in generators:
        fpath = os.path.join(output_dir, fname)
        data = create_png(size, size, gen)
        with open(fpath, "wb") as f:
            f.write(data)
        print(f"Generated {fname} ({len(data)} bytes)")

if __name__ == "__main__":
    generate_all_images("/tmp/DATA_ADVERSARIAL_GAUNTLET")
