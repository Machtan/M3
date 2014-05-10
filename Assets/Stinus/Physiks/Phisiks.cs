using UnityEngine;
using System.Collections;

public class Phisiks : MonoBehaviour {

	private Vector2 movement = new Vector2(0,0) ;
	public bool isSleeping = false;

	// Use this for initialization
	void Start () 
	{
		//hej
	}
	
	// Update is called once per frame
	void Update ()
	{
		coliderCheck();
	}

	void coliderCheck()
	{
		foreach(Colider col in Colider.Colidere)
		{
			if(col.getIfColidingPoint(transform.position))
				Debug.Log("ja");
			else
				Debug.Log("nej");

		}
	}
}
