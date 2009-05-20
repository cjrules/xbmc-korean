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

#include "stdafx.h"
#include "DVDSubtitleParserSami.h"
#include "DVDCodecs/Overlay/DVDOverlayText.h"
#include "DVDClock.h"
#include "utils/RegExp.h"
#include "DVDStreamInfo.h"

using namespace std;

CDVDSubtitleParserSami::CDVDSubtitleParserSami(CDVDSubtitleStream* pStream, const string& filename)
: CDVDSubtitleParserText(pStream, filename)
{

}

CDVDSubtitleParserSami::~CDVDSubtitleParserSami()
{
	Dispose();
}

bool CDVDSubtitleParserSami::Open(CDVDStreamInfo &hints)
{
	__int64 currentTag;
	int pos;
	int pos2;
	double startTime;

	char line[1024];

	CStdStringW strUTF16;
	CStdStringA strUTF8;

	startTime = -1;
	currentTag = 0;

	CRegExp languages(true);
	if (!languages.RegComp("^\\s*\\.([a-zA-Z]+)\\s+\\{[^}]*\\}"))
		return false;

	CRegExp tags(true);
	if (!tags.RegComp("(<[^>]*>|-->|<!--)"))
		return false;

	CRegExp tagNames(true);
	if (!tagNames.RegComp("^<((?:[/a-zA-Z-]+)+)"))
		return false;

	CRegExp tagOptions(true);
	if (!tagOptions.RegComp("([a-zA-Z]+)[ \t]*=[ \t]*(?:[\"'])?([^\"'> ]+)(?:[\"'])?(?:>)?"))
		return false;

	if (!CDVDSubtitleParserText::Open())
		return false;

	CDVDOverlayText* pOverlay = NULL;
	while (m_pStream->ReadLine(line, sizeof(line)))
	{
		pos=0;
		strUTF8.assign(line, strlen(line));
		if (check_style(currentTag))
		{
			pos2=0;
			while(line[pos2] == ' ' || line[pos2] == '\t')
			{
				pos2++;
			}

			if (line[pos2] == '.')
			{
				// language check
				CStdString languageName;
				pos2 = languages.RegFind(line);
				languageName = languages.GetMatch(1);
				vecLanguages.push_back(languageName.ToLower());

				continue;
			}
		}

		while ((pos=tags.RegFind(strUTF8.c_str(), pos)) > -1)
		{
			// Parse Tags
			CStdString fullTag = tags.GetMatch(0);

			pos2=0;
			if (fullTag == "<!--")
			{
				set_comment(currentTag);
				strUTF8.erase(pos, fullTag.length());
			}
			else if (fullTag == "-->")
			{
				unset_comment(currentTag);
				strUTF8.erase(pos, fullTag.length());
			}
			else if (tagNames.RegFind(fullTag.c_str()) > -1)
			{
				CStdString tagName = tagNames.GetMatch(1);

				tagName.ToLower();
				pos2=0;

				if (tagName.Find("sami") != -1)
				{
					if (tagName[0] == '/')
					{
						unset_sami(currentTag);
					}
					else
					{
						set_sami(currentTag);
					}
					strUTF8.erase(pos, fullTag.length());
				}
				else if (tagName.Find("head") != -1)
				{
					if (tagName[0] == '/')
					{
						unset_head(currentTag);
					}
					else
					{
						set_head(currentTag);
					}
					strUTF8.erase(pos, fullTag.length());
				}
				else if (tagName == "style" || tagName == "/style")
				{
					if (tagName[0] == '/')
					{
						unset_style(currentTag);
					}
					else
					{
						while ((pos2 = tagOptions.RegFind(fullTag.c_str(), pos2)) > -1)
						{
							CStdString tagOptionName = tagOptions.GetMatch(1);
							CStdString tagOptionValue = tagOptions.GetMatch(2);
							pos2 += tagOptionName.length() + tagOptionValue.length();
							tagOptionName.ToLower();
							if (tagOptionName == "type")
							{
								tagOptionValue.ToLower();
								if (tagOptionValue == "text/css")
								{
									set_style(currentTag);
								}
							}
							tagOptionName.clear();
							tagOptionValue.clear();
						}
					}
					strUTF8.erase(pos, fullTag.length());
				}
				else if (tagName.Find("body") != -1)
				{
					if (tagName[0] == '/')
					{
						unset_body(currentTag);
					}
					else
					{
						set_body(currentTag);
					}
					strUTF8.erase(pos, fullTag.length());
				}
				else if (tagName == "b" || tagName == "/b")
				{
					if (tagName[0] == '/')
					{
						unset_b(currentTag);
						strUTF8.erase(pos, fullTag.length());
						strUTF8.insert(pos, "[/B]");
						pos += 4;
					}
					else
					{
						set_b(currentTag);
						strUTF8.erase(pos, fullTag.length());
						strUTF8.insert(pos, "[B]");
						pos += 3;
					}
				}
				else if (tagName == "font" || tagName == "/font")
				{
					if (tagName[0] == '/' && check_font(currentTag))
					{
						unset_font(currentTag);
						strUTF8.erase(pos, fullTag.length());
						strUTF8.insert(pos, "[/COLOR]");
						pos += 8;
					}
					else
					{
						strUTF8.erase(pos, fullTag.length());
						while ((pos2 = tagOptions.RegFind(fullTag.c_str(), pos2)) > -1)
						{
							CStdString tagOptionName = tagOptions.GetMatch(1);
							CStdString tagOptionValue = tagOptions.GetMatch(2);
							pos2 += tagOptionName.length() + tagOptionValue.length();
							tagOptionName.ToLower();
							if (tagOptionName == "color")
							{
								set_font(currentTag);
								CStdString tempColorTag = "[COLOR ";
								tempColorTag += GetColorCode(tagOptionValue);
								tempColorTag += "]";
								strUTF8.insert(pos, tempColorTag.ToUpper());
								pos += tempColorTag.length();
							}
							tagOptionName.clear();
							tagOptionValue.clear();
						}
					}
				}
				else if (tagName == "i" || tagName == "/i")
				{
					if (tagName[0] == '/')
					{
						unset_i(currentTag);
						strUTF8.erase(pos, fullTag.length());
						strUTF8.insert(pos, "[/I]");
						pos += 4;
					}
					else
					{
						set_i(currentTag);
						strUTF8.erase(pos, fullTag.length());
						strUTF8.insert(pos, "[I]");
						pos += 3;
					}
				}
				else if (tagName == "p")
				{
					while ((pos2 = tagOptions.RegFind(fullTag.c_str(), pos2)) > -1)
					{
						CStdString tagOptionName = tagOptions.GetMatch(1);
						CStdString tagOptionValue = tagOptions.GetMatch(2);
						pos2 += tagOptionName.length() + tagOptionValue.length();

						tagOptionName.ToLower();
						if (tagOptionName == "class")
						{
							tagOptionValue.ToLower();
							/*
							if (tagOptionValue == "krcc")
							{
							// Language Select
							}
							*/
						}
						tagOptionName.clear();
						tagOptionValue.clear();
					}
					strUTF8.erase(pos, fullTag.length());
				}
				else if (tagName == "sync")
				{
					while ((pos2 = tagOptions.RegFind(fullTag.c_str(), pos2)) > -1)
					{
						CStdString tagOptionName = tagOptions.GetMatch(1);
						CStdString tagOptionValue = tagOptions.GetMatch(2);
						tagOptionName.ToLower();
						pos2 += tagOptionName.length() + tagOptionValue.length();
						if (tagOptionName == "start")
						{
							startTime = (double)atoi(tagOptionValue.c_str()) * (DVD_TIME_BASE / 1000);
						}
						tagOptionName.clear();
						tagOptionValue.clear();
					}
					strUTF8.erase(pos, fullTag.length());
				}
				else if (tagName == "br")
				{
					strUTF8.erase(pos, fullTag.length());
					strUTF8.insert(pos, "\n");
					pos += 1;
				}
				else
				{
					strUTF8.erase(pos, fullTag.length());
				}
				tagName.clear();
			}
			else
			{
				strUTF8.erase(pos, fullTag.length());
			}
			fullTag.clear();
		}

		if (check_sami(currentTag) && check_body(currentTag) && !check_comment(currentTag) && startTime != -1)
		{
			if (pOverlay && pOverlay->iPTSStartTime != DVD_NOPTS_VALUE && startTime != pOverlay->iPTSStartTime)
			{
				pOverlay->iPTSStopTime  = startTime;
				if (check_font(currentTag))
				{
					pOverlay->AddElement(new CDVDOverlayText::CElementText("[/COLOR]"));
					unset_font(currentTag);
				}
				if (check_b(currentTag))
				{
					pOverlay->AddElement(new CDVDOverlayText::CElementText("[/B]"));
					unset_b(currentTag);
				}
				if (check_i(currentTag))
				{
					pOverlay->AddElement(new CDVDOverlayText::CElementText("[/I]"));
					unset_i(currentTag);
				}
				m_collection.Add(pOverlay);

				pOverlay = new CDVDOverlayText();
				pOverlay->Acquire(); // increase ref count with one so that we can hold a handle to this overlay

				pOverlay->iPTSStartTime = startTime;
				pOverlay->iPTSStopTime  = DVD_NOPTS_VALUE;
			}
			else if (pOverlay == NULL)
			{
				pOverlay = new CDVDOverlayText();
				pOverlay->Acquire(); // increase ref count with one so that we can hold a handle to this overlay

				pOverlay->iPTSStartTime = startTime;
				pOverlay->iPTSStopTime  = DVD_NOPTS_VALUE;
			}
			//strUTF8.assign(text, strlen(text));

			g_charsetConverter.subtitleCharsetToW(strUTF8, strUTF16);
			g_charsetConverter.wToUTF8(strUTF16, strUTF8);
			strUTF8.Trim();
			if (strUTF8.IsEmpty())
				continue;
			// add a new text element to our container
			pOverlay->AddElement(new CDVDOverlayText::CElementText(strUTF8.c_str()));

			strUTF8.clear();
			strUTF16.clear();
		}
	}


	m_pStream->Close();
	return true;
}

CStdString CDVDSubtitleParserSami::GetColorCode(CStdString color_text)
{
	const char * temp;
	int i;

	i = 0;

	if (color_text[0] == '#')
	{
		color_text.erase(0, 1);
		return "FF"+color_text;
	}
	else
	{
		color_text.ToLower();
		int left = 0;
		int right = sizeof(color_table)/sizeof(struct color_table_type);
		int comp;
		temp = color_text.c_str();
		while (left <= right)
		{
			i = (left + right) / 2;
			comp = strcmp(color_table[i].color_string, temp);
			switch(comp)
			{
			case -1:
				left = i + 1;
				break;
			case 0: 
				return color_table[i].color_value;
			case 1: 
				right = i - 1;
				break;
			}
		}
	}
	return "";
}
