function setTheme (mode = 'auto') {
  const userMode = localStorage.getItem('bs-theme');
  console.log('userMode')
  console.log(userMode)
  const sysMode = window.matchMedia('(prefers-color-scheme: light)').matches;
  console.log('sysMode')
  console.log(sysMode)
  const useSystem = mode === 'system' || (!userMode && mode === 'auto');
  console.log('useSystem')
  console.log(useSystem)
  const modeChosen = useSystem ? 'system' : mode === 'dark' || mode === 'light' ? mode : userMode;
  console.log('modeChosen')
  console.log(modeChosen)

  if (useSystem) {
    localStorage.removeItem('bs-theme');
  } else {
    localStorage.setItem('bs-theme', modeChosen);
  }

  document.documentElement.setAttribute('data-bs-theme', useSystem ? (sysMode ? 'light' : 'dark') : modeChosen);
  let modeNotChosen = ''
  if (modeChosen === 'dark') modeNotChosen = 'light'
  if (modeChosen === 'light') modeNotChosen = 'dark'
  document.getElementById(modeChosen).classList.add('d-none');
  document.getElementById(modeNotChosen).classList.remove('d-none');

}

setTheme();
window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', () => setTheme());