#pragma once

/*
 *      Copyright (C) 2005-2008 Team XBMC
 *      http://www.xbmc.org
 *
 *  This Program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2, or (at your option)
 *  any later version.
 *
 *  This Program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with XBMC; see the file COPYING.  If not, write to
 *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
 *  http://www.gnu.org/copyleft/gpl.html
 *
 */

#include "DVDSubtitleParser.h"
#include "DVDSubtitleLineCollection.h"

#define SAMI_VERSION		1.0

/* Supported Tag */
#define SAMI_TAG_SAMI			0x00000001
#define SAMI_TAG_HEAD			0x00000002
#define SAMI_TAG_STYLE			0x00000004
#define SAMI_TAG_BODY			0x00000008

#define SAMI_TAG_B				0x00000010
#define SAMI_TAG_FONT			0x00000020
#define SAMI_TAG_I				0x00000040

#define SAMI_TAG_COMMENT		0x00000080

/* Not necessary checking open/close */
#define SAMI_TAG_BR				0x00000000
#define SAMI_TAG_P				0x00000000
#define SAMI_TAG_SYNC			0x00000000

/* Not Supported yet */
#define SAMI_TAG_TITLE			0x00000000
#define SAMI_TAG_BASEFONT		0x00000000
#define SAMI_TAG_BIG			0x00000000
#define SAMI_TAG_BLOCKQUOTE		0x00000000
#define SAMI_TAG_CAPTION		0x00000000
#define SAMI_TAG_CENTER			0x00000000
#define SAMI_TAG_COL			0x00000000
#define SAMI_TAG_COLGROUP		0x00000000
#define SAMI_TAG_DD				0x00000000
#define SAMI_TAG_DIV			0x00000000
#define SAMI_TAG_DL				0x00000000
#define SAMI_TAG_DT				0x00000000
#define SAMI_TAG_H1				0x00000000
#define SAMI_TAG_H2				0x00000000
#define SAMI_TAG_H3				0x00000000
#define SAMI_TAG_H4				0x00000000
#define SAMI_TAG_H5				0x00000000
#define SAMI_TAG_H6				0x00000000
#define SAMI_TAG_HR				0x00000000
#define SAMI_TAG_IMG			0x00000000
#define SAMI_TAG_LI				0x00000000
#define SAMI_TAG_OL				0x00000000
#define SAMI_TAG_PRE			0x00000000
#define SAMI_TAG_Q				0x00000000
#define SAMI_TAG_S				0x00000000
#define SAMI_TAG_SMALL			0x00000000
#define SAMI_TAG_SPAN			0x00000000
#define SAMI_TAG_SUP			0x00000000
#define SAMI_TAG_TABLE			0x00000000
#define SAMI_TAG_TBODY			0x00000000
#define SAMI_TAG_TD				0x00000000
#define SAMI_TAG_TFOOT			0x00000000
#define SAMI_TAG_TH				0x00000000
#define SAMI_TAG_THEAD			0x00000000
#define SAMI_TAG_TR				0x00000000
#define SAMI_TAG_TT				0x00000000
#define SAMI_TAG_U				0x00000000
#define SAMI_TAG_UL				0x00000000

#define check_tag(a, tag)		((a & SAMI_TAG_##tag) == SAMI_TAG_##tag)
#define check_sami(a)			((a & SAMI_TAG_SAMI) == SAMI_TAG_SAMI)
#define check_head(a)			((a & SAMI_TAG_HEAD) == SAMI_TAG_HEAD)
#define check_style(a)			((a & SAMI_TAG_STYLE) == SAMI_TAG_STYLE)
#define check_body(a)			((a & SAMI_TAG_BODY) == SAMI_TAG_BODY)
#define check_b(a)				((a & SAMI_TAG_B) == SAMI_TAG_B)
#define check_font(a)			((a & SAMI_TAG_FONT) == SAMI_TAG_FONT)
#define check_i(a)				((a & SAMI_TAG_I) == SAMI_TAG_I)
#define check_comment(a)		((a & SAMI_TAG_COMMENT) == SAMI_TAG_COMMENT)

#define set_tag(a, tag)			a = a | SAMI_TAG_##tag
#define set_sami(a)				a = a | SAMI_TAG_SAMI
#define set_head(a)				a = a | SAMI_TAG_HEAD
#define set_style(a)			a = a | SAMI_TAG_STYLE
#define set_body(a)				a = a | SAMI_TAG_BODY
#define set_b(a)				a = a | SAMI_TAG_B
#define set_font(a)				a = a | SAMI_TAG_FONT
#define set_i(a)				a = a | SAMI_TAG_I
#define set_comment(a)			a = a | SAMI_TAG_COMMENT

#define unset_tag(a, tag)		a = a & (~SAMI_TAG_##tag)
#define unset_sami(a)			a = a & (~SAMI_TAG_SAMI)
#define unset_head(a)			a = a & (~SAMI_TAG_HEAD)
#define unset_style(a)			a = a & (~SAMI_TAG_STYLE)
#define unset_body(a)			a = a & (~SAMI_TAG_BODY)
#define unset_b(a)				a = a & (~SAMI_TAG_B)
#define unset_font(a)			a = a & (~SAMI_TAG_FONT)
#define unset_i(a)				a = a & (~SAMI_TAG_I)
#define unset_comment(a)		a = a & (~SAMI_TAG_COMMENT)

class CDVDOverlayText;
class CRegExp;


const struct color_table_type
{
	char color_string[33];
	char color_value[9];
} color_table[] = {
	{"aliceblue", "fff0f8ff"}, 
	{"antiquewhite", "fffaebd7"}, 
	{"aqua", "ff00ffff"}, 
	{"aquamarine", "ff7fffd4"}, 
	{"azure", "fff0ffff"}, 
	{"beige", "fff5f5dc"}, 
	{"bisque", "ffffe4c4"}, 
	{"black", "ff000000"}, 
	{"blanchedalmond", "ffffebcd"}, 
	{"blue", "ff0000ff"}, 
	{"blueviolet", "ff8a2be2"}, 
	{"brown", "ffa52a2a"}, 
	{"burlywood", "ffdeb887"}, 
	{"cadetblue", "ff5f9ea0"}, 
	{"chartreuse", "ff7fff00"}, 
	{"chocolate", "ffd2691e"}, 
	{"coral", "ffff7f50"}, 
	{"cornflowerblue", "ff6495ed"}, 
	{"cornsilk", "fffff8dc"}, 
	{"crimson", "ffdc143c"}, 
	{"cyan", "ff00ffff"}, 
	{"darkblue", "ff00008b"}, 
	{"darkcyan", "ff008b8b"}, 
	{"darkgoldenrod", "ffb8860b"}, 
	{"darkgray", "ffa9a9a9"}, 
	{"darkgreen", "ff006400"}, 
	{"darkkhaki", "ffbdb76b"}, 
	{"darkmagenta", "ff8b008b"}, 
	{"darkolivegreen", "ff556b2f"}, 
	{"darkorange", "ffff8c00"}, 
	{"darkorchid", "ff9932cc"}, 
	{"darkred", "ff8b0000"}, 
	{"darksalmon", "ffe9967a"}, 
	{"darkseagreen", "ff8fbc8f"}, 
	{"darkslateblue", "ff483d8b"}, 
	{"darkslategray", "ff2f4f4f"}, 
	{"darkturquoise", "ff00ced1"}, 
	{"darkviolet", "ff9400d3"}, 
	{"deeppink", "ffff1493"}, 
	{"deepskyblue", "ff00bfff"}, 
	{"dimgray", "ff696969"}, 
	{"dodgerblue", "ff1e90ff"}, 
	{"firebrick", "ffb22222"}, 
	{"floralwhite", "fffffaf0"}, 
	{"forestgreen", "ff228b22"}, 
	{"fuchsia", "ffff00ff"}, 
	{"gainsboro", "ffdcdcdc"}, 
	{"ghostwhite", "fff8f8ff"}, 
	{"gold", "ffffd700"}, 
	{"goldenrod", "ffdaa520"}, 
	{"gray", "ff808080"}, 
	{"green", "ff008000"}, 
	{"greenyellow", "ffadff2f"}, 
	{"honeydew", "fff0fff0"}, 
	{"hotpink", "ffff69b4"}, 
	{"indianred ", "ffcd5c5c"}, 
	{"indigo  ", "ff4b0082"}, 
	{"ivory", "fffffff0"}, 
	{"khaki", "fff0e68c"}, 
	{"lavender", "ffe6e6fa"}, 
	{"lavenderblush", "fffff0f5"}, 
	{"lawngreen", "ff7cfc00"}, 
	{"lemonchiffon", "fffffacd"}, 
	{"lightblue", "ffadd8e6"}, 
	{"lightcoral", "fff08080"}, 
	{"lightcyan", "ffe0ffff"}, 
	{"lightgoldenrodyellow", "fffafad2"}, 
	{"lightgrey", "ffd3d3d3"}, 
	{"lightgreen", "ff90ee90"}, 
	{"lightpink", "ffffb6c1"}, 
	{"lightsalmon", "ffffa07a"}, 
	{"lightseagreen", "ff20b2aa"}, 
	{"lightskyblue", "ff87cefa"}, 
	{"lightslategray", "ff778899"}, 
	{"lightsteelblue", "ffb0c4de"}, 
	{"lightyellow", "ffffffe0"}, 
	{"lime", "ff00ff00"}, 
	{"limegreen", "ff32cd32"}, 
	{"linen", "fffaf0e6"}, 
	{"magenta", "ffff00ff"}, 
	{"maroon", "ff800000"}, 
	{"mediumaquamarine", "ff66cdaa"}, 
	{"mediumblue", "ff0000cd"}, 
	{"mediumorchid", "ffba55d3"}, 
	{"mediumpurple", "ff9370d8"}, 
	{"mediumseagreen", "ff3cb371"}, 
	{"mediumslateblue", "ff7b68ee"}, 
	{"mediumspringgreen", "ff00fa9a"}, 
	{"mediumturquoise", "ff48d1cc"}, 
	{"mediumvioletred", "ffc71585"}, 
	{"midnightblue", "ff191970"}, 
	{"mintcream", "fff5fffa"}, 
	{"mistyrose", "ffffe4e1"}, 
	{"moccasin", "ffffe4b5"}, 
	{"navajowhite", "ffffdead"}, 
	{"navy", "ff000080"}, 
	{"oldlace", "fffdf5e6"}, 
	{"olive", "ff808000"}, 
	{"olivedrab", "ff6b8e23"}, 
	{"orange", "ffffa500"}, 
	{"orangered", "ffff4500"}, 
	{"orchid", "ffda70d6"}, 
	{"palegoldenrod", "ffeee8aa"}, 
	{"palegreen", "ff98fb98"}, 
	{"paleturquoise", "ffafeeee"}, 
	{"palevioletred", "ffd87093"}, 
	{"papayawhip", "ffffefd5"}, 
	{"peachpuff", "ffffdab9"}, 
	{"peru", "ffcd853f"}, 
	{"pink", "ffffc0cb"}, 
	{"plum", "ffdda0dd"}, 
	{"powderblue", "ffb0e0e6"}, 
	{"purple", "ff800080"}, 
	{"red", "ffff0000"}, 
	{"rosybrown", "ffbc8f8f"}, 
	{"royalblue", "ff4169e1"}, 
	{"saddlebrown", "ff8b4513"}, 
	{"salmon", "fffa8072"}, 
	{"sandybrown", "fff4a460"}, 
	{"seagreen", "ff2e8b57"}, 
	{"seashell", "fffff5ee"}, 
	{"sienna", "ffa0522d"}, 
	{"silver", "ffc0c0c0"}, 
	{"skyblue", "ff87ceeb"}, 
	{"slateblue", "ff6a5acd"}, 
	{"slategray", "ff708090"}, 
	{"snow", "fffffafa"}, 
	{"springgreen", "ff00ff7f"}, 
	{"steelblue", "ff4682b4"}, 
	{"tan", "ffd2b48c"}, 
	{"teal", "ff008080"}, 
	{"thistle", "ffd8bfd8"}, 
	{"tomato", "ffff6347"}, 
	{"turquoise", "ff40e0d0"}, 
	{"violet", "ffee82ee"}, 
	{"wheat", "fff5deb3"}, 
	{"white", "ffffffff"}, 
	{"whitesmoke", "fff5f5f5"}, 
	{"yellow", "ffffff00"}, 
	{"yellowgreen", "ff9acd32"},
	{"", ""},
};

class CDVDSubtitleParserSami : public CDVDSubtitleParserText
{
public:
  CDVDSubtitleParserSami(CDVDSubtitleStream* pStream, const std::string& strFile);
  virtual ~CDVDSubtitleParserSami();
  virtual bool Open(CDVDStreamInfo &hints);
  std::vector<CStdString> vecLanguages;

private:
  void AddText(CRegExp& tags, CDVDOverlayText*, const char* data, int len);
  CStdString GetColorCode(CStdString color_text);
};
