using UnityEngine;
using System.Collections;

public class Misil : MonoBehaviour {

	// Use this for initialization
	void Start () 
	{
		rigidbody2D.AddForce(new Vector3(200,100));
	
	}

	void Update () {
		//rigidbody.AddForce(new Vector3(1000,100,0));
	}
}
