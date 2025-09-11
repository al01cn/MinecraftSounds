const mobileAgent = ["iphone", "ipod", "ipad", "android", "mobile", "blackberry", "webos", "incognito", "webmate", "bada", "nokia", "lg", "ucweb", "skyfire"];
const browser = typeof window !== 'undefined' ? window.navigator.userAgent.toLowerCase() : navigator.userAgent.toLowerCase();
let isMobile = false;
for (let i=0; i<mobileAgent.length; i++)
{
    if(browser.indexOf(mobileAgent[i])!=-1)
    {
        isMobile = true;
        break;
    }
}
export default isMobile