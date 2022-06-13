def remove_Occ(s, ch):
  for i in range(len(s)):
    if s[i] == ch:
      s = (s[0:i:] + s[(i + 1)::])
      ch += 1
  if ch == 2:
    s = s(ch)
  if ch[(i + len(ch))] == s:
    len(ch)