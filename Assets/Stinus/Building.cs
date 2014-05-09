using UnityEngine;
using System.Collections;

public class Building : MonoBehaviour {

	public Transform BuildingBlock;
	private int blockSide = 16;

	public int width = 4;
	public int height = 8;

	// Use this for initialization
	void Start () 
	{
		spawnBuilding();
	}

	void spawnBuilding()
	{
		for(int i = 0; i < width; i++)
			for(int j = 0; j < height; j++)
			{
				Transform t = Instantiate(BuildingBlock,
			            transform.position + new Vector3(	(float)(i * blockSide) + (float)blockSide / 2f,
			                                 				(float)(j * blockSide) + (float)blockSide / 2f,
			                                 					0),
			            transform.rotation)as Transform;

				t.parent = transform;
			}
	}
	
	// Update is called once per frame
	void Update () {
	
	}
}
