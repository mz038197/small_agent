// Fix: add name parameter to each svgToImg call
const fs = require('fs');
let c = fs.readFileSync('build-presentation.js', 'utf8');

// Map function name to illustration name
const names = [
  ['wg01Illus', 'wg01'],
  ['wg0203Illus', 'wg0203'],
  ['wg04Illus', 'wg04'],
  ['wg05Illus', 'wg05'],
  ['wg0607Illus', 'wg0607'],
  ['wg08Illus', 'wg08'],
  ['wg09Illus', 'wg09'],
  ['wg10Illus', 'wg10'],
  ['wg11Illus', 'wg11'],
  ['wg12Illus', 'wg12'],
  ['wg13Illus', 'wg13'],
  ['wg14Illus', 'wg14'],
  ['wg15Illus', 'wg15'],
  ['wg16Illus', 'wg16'],
  ['wg17Illus', 'wg17'],
];

// Each function currently has: return svgToImg(`<svg ...`);
// We need to change it to: return svgToImg(`<svg ...`, "wgXX");
// The closing is: </svg>`);
// We need to change to: </svg>`, "wgXX");

for (const [funcName, illusName] of names) {
  // Find the function and update its svgToImg closing call
  const oldClose = `    </svg>\`);
}

function ${funcName.includes('wg17') ? '' : names[names.findIndex(n=>n[0]===funcName)+1]?.[0] || 'END'}`;
  // Simpler approach: replace the specific closing for each function
  // by finding the function block
  const funcStart = `function ${funcName}() {\n  return svgToImg(\``;
  const funcIdx = c.indexOf(funcStart);
  if (funcIdx === -1) {
    console.log(`NOT FOUND: ${funcName}`);
    continue;
  }
  // Find the closing `);` after the SVG
  const closingOld = `    </svg>\`);`;
  const closingNew = `    </svg>\`, "${illusName}");`;
  // Find it after funcIdx
  const afterFunc = c.indexOf(closingOld, funcIdx);
  if (afterFunc === -1) {
    console.log(`CLOSING NOT FOUND for: ${funcName}`);
    continue;
  }
  c = c.slice(0, afterFunc) + closingNew + c.slice(afterFunc + closingOld.length);
  console.log(`Fixed: ${funcName} -> ${illusName}`);
}

fs.writeFileSync('build-presentation.js', c, 'utf8');
console.log('Done.');
