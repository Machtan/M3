using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class UpgradeScript : MonoBehaviour {

	private Dictionary<UpgradeSlot, Upgrade> upgrades; // These are assigned from code
	public Dictionary<UpgradeSlot, GameObject> slotCenters; // Where each slot should map to on the character
	public GameObject eyeCenter;

	// Use this for initialization
	void Start () {
		upgrades = new Dictionary<UpgradeSlot, Upgrade>();
		slotCenters = new Dictionary<UpgradeSlot, GameObject>();
		slotCenters.Add (UpgradeSlot.Eyes, eyeCenter);
		AddUpgrade(new LaserEyes());
	}

	void AddUpgrade(Upgrade upgrade) {
		upgrades.Add (upgrade.slot, upgrade);
		if (!slotCenters.ContainsKey(upgrade.slot)) {
			throw new System.Exception("Assign the position of slot '"+upgrade.slot+"' before adding upgrades to it!");
		}
		GameObject transformParent = new GameObject();

		transformParent.transform.position = slotCenters[upgrade.slot].transform.position;
		transformParent.transform.parent = gameObject.transform; // Attach it to the Kaijuu

		GameObject shown = QuickSprite.CreateSprite(upgrade.appearance, slotCenters[upgrade.slot].transform.position);
		shown.transform.parent = transformParent.transform;

		upgrade.Start(gameObject, shown, transformParent.transform);
	}

	void RemoveUpgrade(Upgrade upgrade) {
		if (upgrades[upgrade.slot] == upgrade) {
			upgrades.Remove(upgrade.slot);
		}
	}

	void Update() {
		foreach (Upgrade upgrade in upgrades.Values) {
			upgrade.Update();
		}
	}
}
