var radius_1 = "{{first_element_radius}}"
var radius_2 = "{{second_element_radius}}"

document.addEventListener('DOMContentLoaded', function() {
    const atom1 = document.getElementById('atom1');
    const atom2 = document.getElementById('atom2');
  
    // Set initial positions of the atoms
    atom1.style.left = '100px';
    atom1.style.top = '100px';
    atom2.style.left = '300px';
    atom2.style.top = '100px';
  
    // Move the atoms closer to simulate bond formation
    function moveAtoms() {
      const atom1X = parseInt(atom1.style.left, 10);
      const atom2X = parseInt(atom2.style.left, 10);
  
      if (atom1X < atom2X) {
        atom1.style.left = (atom1X + 1) + 'px';
        atom2.style.left = (atom2X - 1) + 'px';
      } else {
        nterval(intervalId);clearI
      }
    }
  
    // Start the movement animation
    const intervalId = setInterval(moveAtoms, 10);
  });

zoomAtom1 = document.getElementById("zoom1")
zoomAtom1.style.transform = "scale("+radius_1+")"

zoomAtom2 = document.getElementById("zoom2")
zoomAtom2.style.transform = "scale("+radius_2+")"
