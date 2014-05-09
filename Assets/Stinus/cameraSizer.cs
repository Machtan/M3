using UnityEngine;
using System.Collections;

public class cameraSizer : MonoBehaviour {

	void Awake () {
		
		camera.orthographicSize = (Screen.height / 2 );
		
	}
}
