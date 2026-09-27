// Recalibration script: measures advance widths the way iMessage renders them.
//
// You do NOT need to run this to use the library. metrics/advances.json
// ships pre-calibrated. This exists so anyone can verify or regenerate the
// table on their own Mac if Apple ever changes font rendering.
//
// Usage: swift metrics/measure.swift
// Output: "U+XXXX adv=<points> [<font actually used>]" lines, one per char.
// Divide adv by the base size (17.0) to get em values for advances.json.

import Foundation
import CoreText

let baseSize = 17.0
let baseFont = CTFontCreateWithName("SFProText-Regular" as CFString, baseSize, nil)

// codepoints to measure: extend this list when art uses new characters
let codepoints: [UInt32] = [
    0x3000,                         // IDEOGRAPHIC SPACE (grid spacer)
    0xFF3F, 0xFFE3, 0xFF0F, 0xFF3C, // ＿ ￣ ／ ＼
    0xFF5C, 0xFF2F,                 // ｜ Ｏ
    0xFF08, 0xFF09, 0xFF0D,         // （ ） －
    0x3001, 0x3002,                 // 、 。
    0x2588,                         // █ block
    0x2003, 0x2002, 0x2009, 0x200A, // em/en/thin/hair spaces
    0x0020,                         // regular space
    0x1F404,                        // 🐄 the cow that broke everything
]

for code in codepoints {
    let str = String(UnicodeScalar(code)!)
    let attrs: [CFString: Any] = [kCTFontAttributeName: baseFont]
    let attrStr = CFAttributedStringCreate(nil, str as CFString, attrs as CFDictionary)!
    let line = CTLineCreateWithAttributedString(attrStr)
    let runs = CTLineGetGlyphRuns(line) as! [CTRun]
    if runs.isEmpty { print(String(format: "U+%04X: NO RUN", code)); continue }
    var adv = CGSize.zero
    CTRunGetAdvances(runs[0], CFRangeMake(0, 1), &adv)
    let rattrs = CTRunGetAttributes(runs[0]) as NSDictionary
    let usedFont = rattrs[kCTFontAttributeName] as! CTFont
    let usedName = CTFontCopyPostScriptName(usedFont) as String? ?? "?"
    let em = adv.width / baseSize
    print(String(format: "U+%04X adv=%.2fpt (%.4fem) [%@]", code, adv.width, em, usedName))
}
