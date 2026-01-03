import os
import base64
import json

def get_file_content(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def get_binary_base64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

# Paths
BASE_DIR = 'cubarimoe/proxy/static'
JS_DIR = os.path.join(BASE_DIR, 'js')
CSS_DIR = os.path.join(BASE_DIR, 'css')
FONT_DIR = os.path.join(BASE_DIR, 'fonts')

# JS Files
js_files = [
    os.path.join(JS_DIR, 'jszip.min.js'),
    os.path.join(JS_DIR, 'pickr.min.js'),
    os.path.join(JS_DIR, 'ResizeSensor.js'),
    os.path.join(JS_DIR, 'alg_lib.js'),
    os.path.join(JS_DIR, 'UI2.js'),
    os.path.join(JS_DIR, 'init.js'),
]

# CSS Files
css_files = [
    os.path.join(CSS_DIR, 'pickr.css'),
    os.path.join(CSS_DIR, 'icons.css'),
    os.path.join(CSS_DIR, 'reader.css'),
]

# Font
font_base64 = get_binary_base64(os.path.join(FONT_DIR, 'guya.woff'))

# Combine CSS
combined_css = ""
for css_file in css_files:
    content = get_file_content(css_file)
    content = content.replace("../fonts/guya.woff?reqlv7", f"data:application/font-woff;base64,{font_base64}")
    combined_css += content + "\n"

# Combine JS
combined_js = ""
for js_file in js_files:
    combined_js += get_file_content(js_file) + "\n"

# HTML Template
reader_html_parts = [
    '<main id="rdr-main" class="" tabindex="-1">',
    '    <aside class="unload">',
    '      <div class="hide-side" data-bind="sidebar_button">',
    '        <div class="hide-side-actual ico-btn"></div>',
    '      </div>',
    '      <header>',
    '        <a href="#" class="ico-btn guya"></a>',
    '        <h1 data-bind="title"><a href="#">Custom Reader</a></h1>',
    '        <button class="ico-btn"></button>',
    '      </header>',
    '      <div class="rdr-aside-buffer" data-bind="rdr_aside_buffer"></div>',
    '      <div class="rdr-aside-content" data-bind="rdr_aside_content">',
    '        <section class="rdr-selector" data-bind="rdr_selector">',
    '          <div class="rdr-selector-top">',
    '            <button data-bind="vol_next" class="rdr-selector-vol ico-btn prev" data-tip="Previous volume"></button>',
    '            <div class="flex-spacer" data-bind="message"></div>',
    '            <button data-bind="download_chapter" class="ico-btn download"></button>',
    '            <div class="download-anchor">',
    '              <div class="download-wrapper hidden" data-bind="download_wrapper">',
    '                <button data-bind="downloading_chapter" class="ico-btn downloading" disabled></button>',
    '                <button data-bind="download_cancel" class="ico-btn download-cancel"></button>',
    '              </div> ', 
    '            </div>', 
    '            <a data-bind="share_button" data-tip="Short link to current page" class="rdr-share ico-btn "></a>',
    '            <button data-bind="jump" class="ico-btn jump"></button>',
    '            <button data-bind="search" class="ico-btn search"></button>',
    '          </div>', 
    '          <div class="rdr-selector-mid">',
    '            <button data-bind="chap_prev" class="rdr-selector-chap ico-btn prev"></button>',
    '            <div class="rdr-vol-wrap" data-bind="selector_vol">',
    '              <label></label>',
    '              <select id="rdr-vol"></select>',
    '            </div>', 
    '            <div class="rdr-chap-wrap" data-bind="selector_chap">',
    '              <label></label>',
    '              <select id="rdr-chap"></select>',
    '            </div>', 
    '            <button data-bind="chap_next" class="rdr-selector-chap ico-btn next"></button>',
    '          </div>', 
    '          <div class="rdr-selector-bot">',
    '            <button data-bind="vol_prev" class="rdr-selector-vol ico-btn next" data-tip="Next volume"></button>',
    '            <div class="flex-spacer"></div>',
    '            <button data-bind="preload_button" class="ico-btn hidden"></button>',
    '            <button data-bind="fit_button" class="ico-btn"></button>',
    '            <button data-bind="layout_button" class="ico-btn"></button>',
    '            <button data-bind="spread_button" class="ico-btn"></button>',
    '            <button data-bind="sel_pin_button" class="ico-btn"></button>',
    '            <button data-bind="settings_button" class="ico-btn"></button>',
    '          </div>', 
    '        </section>', 
    '        <section class="rdr-groups" data-bind="groups">', 
    '        </section>', 
    '        <section class="rdr-previews">', 
    '          <div class="header" data-bind="previews_button">', 
    '            <span>Previews</span>', 
    '            <div class="ico-btn expander"></div>', 
    '          </div>', 
    '          <div data-bind="previews" class="rdr-previews-gallery">', 
    '          </div>', 
    '        </section>', 
    '        <section class="rdr-description">', 
    '          <div data-bind="image_description">', 
    '          </div>', 
    '        </section>', 
    '      </div>', 
    '    </aside>', 
    '    <div class="rdr-page-selector vis" data-bind="page_selector">', 
    '      <div class="rdr-page-selector-counter" data-bind="page_keys_count"></div>', 
    '      <div class="rdr-page-selector-keys" data-bind="page_keys"></div>', 
    '    </div>', 
    '    <content data-bind="image_viewer" class="rdr-area">', 
    '      <div class="preload-entity" data-bind="preload_entity">', 
    '        <img /><img /><img /><img />', 
    '      </div>', 
    '      <div class="rdr-image-wrap" data-bind="image_container" tabindex="-1">', 
    '      </div>', 
    '      <div class="zoom-level refresh-chapter is-hidden" data-bind="random_chapter">', 
    '        <div class="refresh-chapter-note">This is the Blu-ray extras "random chapter".<br>Click this button to reshuffle the chapter.</div>', 
    '        <div class="ico-btn" data-bind="random_chapter_button">↻</div>', 
    '      </div>', 
    '      <div class="hover-prev" data-bind="hover_prev">', 
    '        <div class="hover-wrap">', 
    '          <div class="hover-arrow"></div>', 
    '          <div class="hover-sub"></div>', 
    '        </div>', 
    '      </div>', 
    '      <div class="hover-next" data-bind="hover_next">', 
    '        <div class="hover-wrap">', 
    '          <div class="hover-arrow"></div>', 
    '          <div class="hover-sub"></div>', 
    '        </div>', 
    '      </div>', 
    '    </content>', 
    '    <div class="zoom-level vis" data-bind="zoom_level">', 
    '      <div class="ico-btn" data-bind="zoom_level_plus"></div>', 
    '      <div class="ico-btn" data-bind="zoom_level_minus"></div>', 
    '    </div>', 
    '</main>', 
    '<div class="Tooltippy"></div>', 
    '<div class="Tooltippy Error"></div>', 
    '<div class="LodaManager hidden" tabindex="-1"></div>'
]
reader_html = "\n".join(reader_html_parts)

# Read template
template = get_file_content('userscript_template.js')

# Perform injection
output = template.replace('CSS_PLACEHOLDER', json.dumps(combined_css))
output = output.replace('JS_PLACEHOLDER', json.dumps(combined_js))
output = output.replace('HTML_PLACEHOLDER', json.dumps(reader_html))

# Save final script
with open('cubari_custom_reader.user.js', 'w', encoding='utf-8') as f:
    f.write(output)

print("Tampermonkey script generated: cubari_custom_reader.user.js")
